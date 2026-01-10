import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Copy, Check, Crown, Users, DollarSign } from 'lucide-react';

interface Subscription {
  id: number;
  plan: string;
  status: string;
  expires_at: string;
}

interface Referral {
  code: string;
  total_rewards: number;
  referral_count: number;
}

export default function Profile() {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [referral, setReferral] = useState<Referral | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Fetch subscription and referral data
    const fetchProfileData = async () => {
      try {
        const [subRes, refRes] = await Promise.all([
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/profile/subscription/1`), // User ID placeholder
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/profile/referral/1`)
        ]);
        setSubscription(subRes.data);
        setReferral(refRes.data);
      } catch (error) {
        console.error('Error fetching profile data:', error);
      }
    };

    fetchProfileData();
  }, []);

  const copyReferralCode = async () => {
    if (referral?.code) {
      await navigator.clipboard.writeText(referral.code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const generateReferralCode = async () => {
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/profile/referral/generate/1`);
      setReferral(response.data);
    } catch (error) {
      console.error('Error generating referral code:', error);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Profile</h1>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Subscription */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Crown className="mr-2 h-5 w-5" />
              Subscription
            </CardTitle>
          </CardHeader>
          <CardContent>
            {subscription ? (
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">Plan: {subscription.plan}</p>
                <p className="text-sm text-muted-foreground">Status: {subscription.status}</p>
                <p className="text-sm text-muted-foreground">
                  Expires: {new Date(subscription.expires_at).toLocaleDateString()}
                </p>
                <Button className="w-full">Upgrade Plan</Button>
              </div>
            ) : (
              <div className="text-center py-8">
                <Crown className="mx-auto h-12 w-12 mb-4 opacity-50" />
                <p className="text-muted-foreground mb-4">No active subscription</p>
                <Button>Get Started</Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Referral System */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="mr-2 h-5 w-5" />
              Referral Program
            </CardTitle>
          </CardHeader>
          <CardContent>
            {referral ? (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="referral-code">Referral Code</Label>
                  <div className="flex mt-1">
                    <Input
                      id="referral-code"
                      value={referral.code}
                      readOnly
                      className="font-mono"
                    />
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={copyReferralCode}
                      className="ml-2"
                    >
                      {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold">{referral.referral_count}</p>
                    <p className="text-sm text-muted-foreground">Referrals</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold flex items-center justify-center">
                      <DollarSign className="h-4 w-4 mr-1" />
                      {referral.total_rewards.toFixed(2)}
                    </p>
                    <p className="text-sm text-muted-foreground">Rewards</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <Users className="mx-auto h-12 w-12 mb-4 opacity-50" />
                <p className="text-muted-foreground mb-4">Generate your referral code</p>
                <Button onClick={generateReferralCode}>Generate Code</Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
