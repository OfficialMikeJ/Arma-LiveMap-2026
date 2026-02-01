import { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import MapPage from './pages/MapPage';
import { User } from './types';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const checkSession = async () => {
      const savedToken = localStorage.getItem('session_token');
      if (savedToken) {
        // Session validation would happen here
        // For now, just clear it
        setLoading(false);
      } else {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const handleLogin = (userData: User, token: string) => {
    setUser(userData);
    localStorage.setItem('session_token', token);
  };

  const handleLogout = async () => {
    if (user) {
      await window.electronAPI.logout(user.id);
      localStorage.removeItem('session_token');
      setUser(null);
    }
  };

  if (loading) {
    return (
      <div className="w-full h-screen flex items-center justify-center bg-tactical-bg">
        <div className="text-military-500 text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="w-full h-screen bg-tactical-bg">
      {user ? (
        <MapPage user={user} onLogout={handleLogout} />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
