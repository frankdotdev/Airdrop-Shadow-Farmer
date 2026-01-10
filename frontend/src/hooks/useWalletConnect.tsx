import { useState, useEffect } from 'react';
import WalletConnect from '@walletconnect/web3-provider';

export const useWalletConnect = () => {
  const [provider, setProvider] = useState<any>(null);
  const [connected, setConnected] = useState(false);

  const connect = async () => {
    const wcProvider = new WalletConnect({
      infuraId: 'your-infura-id', // Placeholder
      qrcodeModal: true,
    });
    await wcProvider.enable();
    setProvider(wcProvider);
    setConnected(true);
  };

  const disconnect = async () => {
    if (provider) {
      await provider.disconnect();
      setConnected(false);
    }
  };

  const signTransaction = async (tx: any) => {
    if (provider) {
      const web3 = new (await import('web3')).default(provider);
      const accounts = await web3.eth.getAccounts();
      const signedTx = await web3.eth.signTransaction(tx, accounts[0]);
      return signedTx;
    }
  };

  return { connect, disconnect, signTransaction, connected };
};
