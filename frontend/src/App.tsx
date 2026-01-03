import { useEffect } from 'react';
import { initUtils } from '@twa-dev/sdk';

function App() {
  useEffect(() => {
    initUtils();
  }, []);

  return (
    <div className="bg-gray-900 text-white">
      <h1>Shadow Farmer Dashboard</h1>
      {/* Add Bento Grid, Tabs, etc. using shadcn */}
    </div>
  );
}

export default App;