import * as crypto from 'crypto';
import * as speakeasy from 'speakeasy';
import * as QRCode from 'qrcode';
import { DatabaseService, User } from './database';

export class AuthService {
  private db: DatabaseService;

  constructor(db: DatabaseService) {
    this.db = db;
  }

  async register(username: string, password: string, securityQuestions: Array<{ question: string; answer: string }>) {
    try {
      // Check if user exists
      const existingUser = this.db.getUserByUsername(username);
      if (existingUser) {
        return { success: false, error: 'Username already exists' };
      }

      // Hash password
      const passwordHash = crypto.createHash('sha256').update(password).digest('hex');

      // Create user
      const userId = this.db.createUser(username, passwordHash);

      // Save security questions
      this.db.saveSecurityQuestions(userId, securityQuestions);

      return { success: true, userId };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async login(username: string, password: string) {
    try {
      const user = this.db.getUserByUsername(username);
      if (!user) {
        return { success: false, error: 'Invalid credentials' };
      }

      const passwordHash = crypto.createHash('sha256').update(password).digest('hex');
      if (user.password_hash !== passwordHash) {
        return { success: false, error: 'Invalid credentials' };
      }

      // Create session token
      const token = crypto.randomBytes(32).toString('hex');
      const deviceId = crypto.randomBytes(16).toString('hex');
      const expiresAt = new Date();
      expiresAt.setDate(expiresAt.getDate() + 60); // 60 days

      this.db.createSession(user.id, token, deviceId, expiresAt);

      return {
        success: true,
        user: {
          id: user.id,
          username: user.username,
          hasTOTP: !!user.totp_secret
        },
        token
      };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async logout(userId: number) {
    try {
      this.db.deleteSession(userId);
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async enableTOTP(userId: number) {
    try {
      const user = this.db.getUserById(userId);
      if (!user) {
        return { success: false, error: 'User not found' };
      }

      // Generate TOTP secret
      const secret = speakeasy.generateSecret({
        name: `ArmaReforgerMap (${user.username})`,
        issuer: 'Arma Reforger Tactical Map'
      });

      // Generate QR code
      const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url!);

      // Save secret to database
      this.db.updateTOTPSecret(userId, secret.base32);

      return {
        success: true,
        secret: secret.base32,
        qrCode: qrCodeUrl
      };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async verifyTOTP(userId: number, token: string) {
    try {
      const user = this.db.getUserById(userId);
      if (!user || !user.totp_secret) {
        return { success: false, error: 'TOTP not enabled' };
      }

      const verified = speakeasy.totp.verify({
        secret: user.totp_secret,
        encoding: 'base32',
        token: token,
        window: 2
      });

      return { success: verified };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async verifySession(token: string) {
    try {
      const session = this.db.getSessionByToken(token);
      if (!session) {
        return { success: false, error: 'Invalid session' };
      }

      const user = this.db.getUserById(session.user_id);
      if (!user) {
        return { success: false, error: 'User not found' };
      }

      return {
        success: true,
        user: {
          id: user.id,
          username: user.username,
          hasTOTP: !!user.totp_secret
        }
      };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }
}
