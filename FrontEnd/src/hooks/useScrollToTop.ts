import { useEffect } from 'react';

interface UseScrollToTopOptions {
  behavior?: 'auto' | 'smooth';
  top?: number;
  left?: number;
  trigger?: any; // Any dependency that should trigger scroll
}

/**
 * Custom hook to scroll to top of the page
 * Can be used in individual components for more granular control
 */
export const useScrollToTop = (options: UseScrollToTopOptions = {}) => {
  const { behavior = 'auto', top = 0, left = 0, trigger } = options;

  useEffect(() => {
    window.scrollTo({
      top,
      left,
      behavior,
    });
  }, [trigger, behavior, top, left]);

  // Return a function to manually trigger scroll to top
  const scrollToTop = () => {
    window.scrollTo({
      top,
      left,
      behavior,
    });
  };

  return scrollToTop;
};

/**
 * Utility function to scroll to top
 * Can be called imperatively from event handlers
 */
export const scrollToTop = (options: UseScrollToTopOptions = {}) => {
  const { behavior = 'auto', top = 0, left = 0 } = options;
  
  window.scrollTo({
    top,
    left,
    behavior,
  });
};
