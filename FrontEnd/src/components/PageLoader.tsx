import React from 'react';

const loaderGif = "/src/assets/loading.gif"

const PageLoader: React.FC = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-white dark:bg-slate-900 z-50">
    <img src={loaderGif} alt="Loading" className="w-32 h-32" />
  </div>
);

export default PageLoader;
