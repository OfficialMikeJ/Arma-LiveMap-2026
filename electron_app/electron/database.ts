import Database from 'better-sqlite3';
import * as crypto from 'crypto';

export interface User {
  id: number;
  username: string;
  password_hash: string;
  totp_secret?: string;
  created_at: string;
}

export interface Marker {
  id: string;
  type: string;
  shape: string;
  x: number;
  y: number;
  color: string;
  created_by: string;
  timestamp: string;
  notes?: string;
}

export interface Server {
  id: number;
  name: string;
  ip_address: string;
  port: number;
  enabled: boolean;
}

export class DatabaseService {
  private db: Database.Database;

  constructor(dbPath: string) {
    this.db = new Database(dbPath);
    this.initialize();
  }

  private initialize() {
    // Users table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        totp_secret TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Security questions
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS security_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer_hash TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    `);

    // Sessions
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        device_id TEXT,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    `);

    // Servers
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip_address TEXT NOT NULL,
        port INTEGER NOT NULL,
        enabled BOOLEAN DEFAULT 1
      )
    `);

    // Insert default server if none exist
    const serverCount = this.db.prepare('SELECT COUNT(*) as count FROM servers').get() as { count: number };
    if (serverCount.count === 0) {
      this.db.prepare(`
        INSERT INTO servers (name, ip_address, port, enabled) VALUES 
        ('Test Server', '192.168.2.26', 2001, 1)
      `).run();
    }

    // Markers
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS markers (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        shape TEXT NOT NULL,
        x REAL NOT NULL,
        y REAL NOT NULL,
        color TEXT NOT NULL,
        created_by TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
      )
    `);

    // Feedback
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        message TEXT NOT NULL,
        email TEXT,
        submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
  }

  // User methods
  getUserByUsername(username: string): User | undefined {
    return this.db.prepare('SELECT * FROM users WHERE username = ?').get(username) as User | undefined;
  }

  getUserById(id: number): User | undefined {
    return this.db.prepare('SELECT * FROM users WHERE id = ?').get(id) as User | undefined;
  }

  createUser(username: string, passwordHash: string): number {
    const result = this.db.prepare('INSERT INTO users (username, password_hash) VALUES (?, ?)').run(username, passwordHash);
    return result.lastInsertRowid as number;
  }

  saveSecurityQuestions(userId: number, questions: Array<{ question: string; answer: string }>) {
    const stmt = this.db.prepare('INSERT INTO security_questions (user_id, question, answer_hash) VALUES (?, ?, ?)');
    for (const q of questions) {
      const answerHash = crypto.createHash('sha256').update(q.answer.toLowerCase()).digest('hex');
      stmt.run(userId, q.question, answerHash);
    }
  }

  updateTOTPSecret(userId: number, secret: string) {
    this.db.prepare('UPDATE users SET totp_secret = ? WHERE id = ?').run(secret, userId);
  }

  // Session methods
  createSession(userId: number, token: string, deviceId: string, expiresAt: Date) {
    this.db.prepare('INSERT INTO sessions (user_id, token, device_id, expires_at) VALUES (?, ?, ?, ?)').run(userId, token, deviceId, expiresAt.toISOString());
  }

  getSessionByToken(token: string) {
    return this.db.prepare('SELECT * FROM sessions WHERE token = ? AND expires_at > datetime("now")').get(token);
  }

  deleteSession(userId: number) {
    this.db.prepare('DELETE FROM sessions WHERE user_id = ?').run(userId);
  }

  // Marker methods
  getAllMarkers(): Marker[] {
    return this.db.prepare('SELECT * FROM markers ORDER BY timestamp DESC').all() as Marker[];
  }

  addMarker(marker: Marker): boolean {
    try {
      this.db.prepare(`
        INSERT INTO markers (id, type, shape, x, y, color, created_by, timestamp, notes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).run(marker.id, marker.type, marker.shape, marker.x, marker.y, marker.color, marker.created_by, marker.timestamp, marker.notes || null);
      return true;
    } catch (error) {
      console.error('Error adding marker:', error);
      return false;
    }
  }

  removeMarker(markerId: string): boolean {
    try {
      this.db.prepare('DELETE FROM markers WHERE id = ?').run(markerId);
      return true;
    } catch (error) {
      console.error('Error removing marker:', error);
      return false;
    }
  }

  clearMarkers() {
    this.db.prepare('DELETE FROM markers').run();
  }

  // Server methods
  getAllServers(): Server[] {
    return this.db.prepare('SELECT * FROM servers').all() as Server[];
  }

  saveServers(servers: Server[]): boolean {
    try {
      // Delete all and re-insert
      this.db.prepare('DELETE FROM servers').run();
      const stmt = this.db.prepare('INSERT INTO servers (id, name, ip_address, port, enabled) VALUES (?, ?, ?, ?, ?)');
      for (const server of servers) {
        stmt.run(server.id, server.name, server.ip_address, server.port, server.enabled ? 1 : 0);
      }
      return true;
    } catch (error) {
      console.error('Error saving servers:', error);
      return false;
    }
  }

  // Feedback methods
  saveFeedback(feedback: { type: string; message: string; email?: string }): boolean {
    try {
      this.db.prepare('INSERT INTO feedback (type, message, email) VALUES (?, ?, ?)').run(feedback.type, feedback.message, feedback.email || null);
      return true;
    } catch (error) {
      console.error('Error saving feedback:', error);
      return false;
    }
  }

  close() {
    this.db.close();
  }
}
