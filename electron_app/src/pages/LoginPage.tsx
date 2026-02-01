import { useState } from 'react';
import { User, SecurityQuestion } from '../types';

interface Props {
  onLogin: (user: User, token: string) => void;
}

export default function LoginPage({ onLogin }: Props) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Security questions for registration
  const [secQ1, setSecQ1] = useState('What was your first pet\'s name?');
  const [secA1, setSecA1] = useState('');
  const [secQ2, setSecQ2] = useState('What city were you born in?');
  const [secA2, setSecA2] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await window.electronAPI.login(username, password);
      if (result.success) {
        onLogin(result.user, result.token);
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 4) {
      setError('Password must be at least 4 characters');
      return;
    }

    if (!secA1 || !secA2) {
      setError('Please answer both security questions');
      return;
    }

    setLoading(true);

    try {
      const securityQuestions: SecurityQuestion[] = [
        { question: secQ1, answer: secA1 },
        { question: secQ2, answer: secA2 }
      ];

      const result = await window.electronAPI.register(username, password, securityQuestions);
      if (result.success) {
        // Auto-login after registration
        const loginResult = await window.electronAPI.login(username, password);
        if (loginResult.success) {
          onLogin(loginResult.user, loginResult.token);
        }
      } else {
        setError(result.error || 'Registration failed');
      }
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-tactical-bg to-military-900">
      <div className="w-full max-w-md p-8">
        <div className="card">
          <h1 className="text-3xl font-bold text-center mb-2 text-military-500">
            Arma Reforger
          </h1>
          <h2 className="text-xl text-center mb-6 text-tactical-text">
            Tactical Map
          </h2>

          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-2 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={isRegister ? handleRegister : handleLogin}>
            <div className="mb-4">
              <label className="block text-tactical-text mb-2">Username</label>
              <input
                type="text"
                className="input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                minLength={3}
                disabled={loading}
              />
            </div>

            <div className="mb-4">
              <label className="block text-tactical-text mb-2">Password</label>
              <input
                type="password"
                className="input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={4}
                disabled={loading}
              />
            </div>

            {isRegister && (
              <>
                <div className="mb-4">
                  <label className="block text-tactical-text mb-2">Confirm Password</label>
                  <input
                    type="password"
                    className="input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    disabled={loading}
                  />
                </div>

                <div className="mb-4">
                  <label className="block text-tactical-text mb-2">Security Question 1</label>
                  <select
                    className="input mb-2"
                    value={secQ1}
                    onChange={(e) => setSecQ1(e.target.value)}
                    disabled={loading}
                  >
                    <option>What was your first pet's name?</option>
                    <option>What city were you born in?</option>
                    <option>What is your mother's maiden name?</option>
                  </select>
                  <input
                    type="text"
                    className="input"
                    placeholder="Answer"
                    value={secA1}
                    onChange={(e) => setSecA1(e.target.value)}
                    required
                    disabled={loading}
                  />
                </div>

                <div className="mb-4">
                  <label className="block text-tactical-text mb-2">Security Question 2</label>
                  <select
                    className="input mb-2"
                    value={secQ2}
                    onChange={(e) => setSecQ2(e.target.value)}
                    disabled={loading}
                  >
                    <option>What city were you born in?</option>
                    <option>What was your first pet's name?</option>
                    <option>What is your favorite color?</option>
                  </select>
                  <input
                    type="text"
                    className="input"
                    placeholder="Answer"
                    value={secA2}
                    onChange={(e) => setSecA2(e.target.value)}
                    required
                    disabled={loading}
                  />
                </div>
              </>
            )}

            <button
              type="submit"
              className="btn btn-primary w-full mb-3"
              disabled={loading}
            >
              {loading ? 'Please wait...' : (isRegister ? 'Register' : 'Login')}
            </button>

            <button
              type="button"
              className="btn btn-secondary w-full"
              onClick={() => {
                setIsRegister(!isRegister);
                setError('');
              }}
              disabled={loading}
            >
              {isRegister ? 'Back to Login' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-tactical-text opacity-70">
            Version 1.0.0
          </div>
        </div>
      </div>
    </div>
  );
}
