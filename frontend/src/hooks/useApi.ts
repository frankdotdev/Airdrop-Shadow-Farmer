import { useState, useEffect } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const useApi = () => {
  return api;
};

export const useWallets = () => {
  const [wallets, setWallets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWallets = async () => {
      try {
        const response = await api.get('/wallets');
        setWallets(response.data);
      } catch (error) {
        console.error('Error fetching wallets:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWallets();
  }, []);

  const addWallet = async (walletData: any) => {
    try {
      const response = await api.post('/wallets', walletData);
      setWallets([...wallets, response.data]);
      return response.data;
    } catch (error) {
      console.error('Error adding wallet:', error);
      throw error;
    }
  };

  return { wallets, loading, addWallet };
};

export const useStrategies = () => {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStrategies = async () => {
      try {
        const response = await api.get('/strategies');
        setStrategies(response.data);
      } catch (error) {
        console.error('Error fetching strategies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStrategies();
  }, []);

  const startStrategy = async (strategyId: number) => {
    try {
      await api.post(`/strategies/${strategyId}/start`);
      setStrategies(strategies.map((s: any) => s.id === strategyId ? { ...s, active: true } : s));
    } catch (error) {
      console.error('Error starting strategy:', error);
      throw error;
    }
  };

  const stopStrategy = async (strategyId: number) => {
    try {
      await api.post(`/strategies/${strategyId}/stop`);
      setStrategies(strategies.map((s: any) => s.id === strategyId ? { ...s, active: false } : s));
    } catch (error) {
      console.error('Error stopping strategy:', error);
      throw error;
    }
  };

  return { strategies, loading, startStrategy, stopStrategy };
};

export const useActivityFeed = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await api.get('/activities');
        setActivities(response.data);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
    const interval = setInterval(fetchActivities, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return { activities, loading };
};
