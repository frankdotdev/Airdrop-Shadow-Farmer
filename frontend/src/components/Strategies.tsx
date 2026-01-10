import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Slider } from './ui/slider';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Play, Pause, Settings, Zap } from 'lucide-react';

interface Strategy {
  id: number;
  name: string;
  aggression: number;
  gasGuard: boolean;
  active: boolean;
}

interface AirdropOpportunity {
  id: string;
  token: string;
  value: number;
  risk: string;
}

export default function Strategies() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [airdrops, setAirdrops] = useState<AirdropOpportunity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch strategies
        const strategiesResponse = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/strategies/list`);
        setStrategies(strategiesResponse.data);

        // Fetch airdrop opportunities
        const airdropsResponse = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/scan`);
        setAirdrops(airdropsResponse.data);
      } catch (error) {
        console.error('Error fetching strategies data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const updateStrategy = async (id: number, updates: Partial<Strategy>) => {
    try {
      await axios.put(`${import.meta.env.VITE_API_BASE_URL}/strategies/${id}`, updates);
      setStrategies(strategies.map(s => s.id === id ? { ...s, ...updates } : s));
    } catch (error) {
      console.error('Error updating strategy:', error);
    }
  };

  const startFarming = async (strategyId: number) => {
    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/farming/start`, { strategy_id: strategyId });
      updateStrategy(strategyId, { active: true });
    } catch (error) {
      console.error('Error starting farming:', error);
    }
  };

  const stopFarming = async (strategyId: number) => {
    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/farming/stop`, { strategy_id: strategyId });
      updateStrategy(strategyId, { active: false });
    } catch (error) {
      console.error('Error stopping farming:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-8 text-foreground">Strategies</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader className="pb-2">
                  <div className="h-6 bg-muted rounded w-3/4"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="h-4 bg-muted rounded w-full"></div>
                    <div className="h-4 bg-muted rounded w-2/3"></div>
                    <div className="h-8 bg-muted rounded w-1/3"></div>
                  </div>
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
        <h1 className="text-3xl font-bold mb-8 text-foreground">Strategies</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Strategies Cards */}
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-foreground">Farming Strategies</h2>
            {strategies.map(strategy => (
              <Card key={strategy.id} className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{strategy.name}</span>
                    <div className="flex items-center space-x-2">
                      {strategy.active ? (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => stopFarming(strategy.id)}
                        >
                          <Pause className="mr-2 h-4 w-4" />
                          Stop
                        </Button>
                      ) : (
                        <Button
                          variant="default"
                          size="sm"
                          onClick={() => startFarming(strategy.id)}
                        >
                          <Play className="mr-2 h-4 w-4" />
                          Start
                        </Button>
                      )}
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor={`aggression-${strategy.id}`}>Aggression Level: {strategy.aggression}</Label>
                    <Slider
                      id={`aggression-${strategy.id}`}
                      min={1}
                      max={10}
                      step={1}
                      value={[strategy.aggression]}
                      onValueChange={(value) => updateStrategy(strategy.id, { aggression: value[0] })}
                      className="mt-2"
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id={`gasguard-${strategy.id}`}
                      checked={strategy.gasGuard}
                      onCheckedChange={(checked) => updateStrategy(strategy.id, { gasGuard: checked })}
                    />
                    <Label htmlFor={`gasguard-${strategy.id}`} className="flex items-center">
                      <Zap className="mr-2 h-4 w-4" />
                      Gas Guard
                    </Label>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Airdrop Scanner */}
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-foreground">Airdrop Scanner</h2>
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Settings className="mr-2 h-5 w-5" />
                  New Opportunities
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {airdrops.length > 0 ? (
                    airdrops.map((airdrop) => (
                      <div key={airdrop.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                        <div>
                          <p className="font-medium text-foreground">{airdrop.token}</p>
                          <p className="text-sm text-muted-foreground">
                            Value: ${airdrop.value.toLocaleString()} | Risk: {airdrop.risk}
                          </p>
                        </div>
                        <Button variant="outline" size="sm">
                          Claim
                        </Button>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <Settings className="mx-auto h-12 w-12 mb-4 opacity-50" />
                      <p>No new opportunities found</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
