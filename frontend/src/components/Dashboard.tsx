import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Activity, DollarSign, Pause, TrendingUp, Wallet, Zap } from 'lucide-react';

interface ActivityLog {
  message: string;
  timestamp: string;
}

interface ProfitData {
  totalValue: number;
  dailyChange: number;
  weeklyChange: number;
}

export default function Dashboard() {
  const [profitData, setProfitData] = useState<ProfitData>({ totalValue: 0, dailyChange: 0, weeklyChange: 0 });
  const [activities, setActivities] = useState<ActivityLog[]>([]);
  const [activeWallets, setActiveWallets] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch profit data from Coingecko API
        const coingeckoResponse = await axios.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd');
        const ethPrice = coingeckoResponse.data.ethereum.usd;

        // Fetch backend status
        const statusResponse = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/status`);
        const backendData = statusResponse.data;

        setProfitData({
          totalValue: backendData.total_value || 0,
          dailyChange: backendData.daily_change || 0,
          weeklyChange: backendData.weekly_change || 0,
        });
        setActivities(backendData.activities || []);
        setActiveWallets(backendData.active_wallets || 0);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();

    // Poll for updates every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-8 text-foreground">Shadow Farmer Dashboard</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader className="pb-2">
                  <div className="h-4 bg-muted rounded w-3/4"></div>
                </CardHeader>
                <CardContent>
                  <div className="h-8 bg-muted rounded w-1/2 mb-2"></div>
                  <div className="h-3 bg-muted rounded w-1/4"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-foreground">Shadow Farmer Dashboard</h1>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Value Card */}
          <Card className="col-span-1 md:col-span-2 lg:col-span-2 bg-card border-border">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <DollarSign className="mr-2 h-5 w-5 text-emerald-500" />
                Total Estimated Value
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground mb-2">
                {formatCurrency(profitData.totalValue)}
              </div>
              <div className="flex items-center space-x-4 text-sm">
                <span className={`flex items-center ${profitData.dailyChange >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                  <TrendingUp className="mr-1 h-3 w-3" />
                  {formatPercentage(profitData.dailyChange)} (24h)
                </span>
                <span className={`flex items-center ${profitData.weeklyChange >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                  <TrendingUp className="mr-1 h-3 w-3" />
                  {formatPercentage(profitData.weeklyChange)} (7d)
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Active Wallets Card */}
          <Card className="bg-card border-border">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <Wallet className="mr-2 h-5 w-5 text-blue-500" />
                Active Wallets
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">{activeWallets}</div>
              <p className="text-sm text-muted-foreground">Currently farming</p>
            </CardContent>
          </Card>

          {/* Gas Efficiency Card */}
          <Card className="bg-card border-border">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <Zap className="mr-2 h-5 w-5 text-yellow-500" />
                Gas Efficiency
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">92%</div>
              <p className="text-sm text-muted-foreground">Optimized transactions</p>
            </CardContent>
          </Card>
        </div>

        {/* Activity Feed */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-2 bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="mr-2 h-5 w-5" />
                Activity Feed
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {activities.length > 0 ? (
                  activities.map((act, idx) => (
                    <div key={idx} className="flex items-start space-x-3 p-3 rounded-lg bg-muted/50">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div className="flex-1">
                        <p className="text-sm text-foreground">{act.message}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {new Date(act.timestamp).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Activity className="mx-auto h-12 w-12 mb-4 opacity-50" />
                    <p>No recent activity</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="destructive" className="w-full">
                <Pause className="mr-2 h-4 w-4" />
                Pause All Farming
              </Button>
              <Button variant="outline" className="w-full">
                <TrendingUp className="mr-2 h-4 w-4" />
                View Analytics
              </Button>
              <Button variant="outline" className="w-full">
                <Wallet className="mr-2 h-4 w-4" />
                Add New Wallet
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
