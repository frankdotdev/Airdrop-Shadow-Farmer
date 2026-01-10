import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Plus, Trash2 } from 'lucide-react';

interface Wallet {
  id: number;
  address: string;
  sybil_score: number;
}

export default function Wallets() {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [newAddress, setNewAddress] = useState('');

  useEffect(() => {
    axios.get('/api/wallets/list/1').then(res => setWallets(res.data)); // User ID placeholder
  }, []);

  const addWallet = () => {
    axios.post('/api/wallets/add', { address: newAddress, session_data: 'mock', user_id: 1 })
      .then(() => {
        setNewAddress('');
        // Refresh list
        axios.get('/api/wallets/list/1').then(res => setWallets(res.data));
      });
  };

  const removeWallet = (id: number) => {
    axios.delete(`/api/wallets/remove/${id}`).then(() => {
      setWallets(wallets.filter(w => w.id !== id));
    });
  };

  return (
    <div className="p-4 bg-gray-900 text-white min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Wallets</h1>
      <div className="mb-4 flex gap-2">
        <Input
          value={newAddress}
          onChange={(e) => setNewAddress(e.target.value)}
          placeholder="Enter wallet address"
          className="bg-gray-800 border-gray-700"
        />
        <Button onClick={addWallet}>
          <Plus className="mr-2" />
          Add
        </Button>
      </div>
      <div className="grid gap-4">
        {wallets.map(wallet => (
          <Card key={wallet.id} className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="font-mono text-sm">{wallet.address}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Sybil Score: {wallet.sybil_score}/100</p>
              <Button variant="destructive" onClick={() => removeWallet(wallet.id)}>
                <Trash2 className="mr-2" />
                Remove
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
