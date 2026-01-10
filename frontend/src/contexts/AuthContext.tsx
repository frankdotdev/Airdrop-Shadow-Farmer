import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { initData, user } from '@twa-dev/sdk';

interface AuthContextType {
  isAuthenticated: boolean;
  userId: string | null;
  initAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  const initAuth = () => {
    try {
      const data = initData;
      if (data && user) {
        setUserId(user.id.toString());
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Auth init failed:', error);
    }
  };

  useEffect(() => {
    initAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, userId, initAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
