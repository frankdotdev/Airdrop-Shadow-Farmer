import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Dashboard from './components/Dashboard';
import Wallets from './components/Wallets';
import Strategies from './components/Strategies';
import Profile from './components/Profile';
import { Button } from './components/ui/button';
import { Card, CardContent } from './components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Link, useLocation } from 'react-router-dom';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-background text-foreground">
          <nav className="border-b border-border bg-card">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <Link to="/dashboard" className="text-xl font-bold text-foreground">
                    Shadow Farmer
                  </Link>
                </div>
                <div className="flex space-x-4">
                  <Link to="/dashboard">
                    <Button variant="ghost">Dashboard</Button>
                  </Link>
                  <Link to="/wallets">
                    <Button variant="ghost">Wallets</Button>
                  </Link>
                  <Link to="/strategies">
                    <Button variant="ghost">Strategies</Button>
                  </Link>
                  <Link to="/profile">
                    <Button variant="ghost">Profile</Button>
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/wallets" element={<Wallets />} />
              <Route path="/strategies" element={<Strategies />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/" element={<Dashboard />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
