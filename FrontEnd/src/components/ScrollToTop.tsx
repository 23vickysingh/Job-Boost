import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

interface ScrollToTopProps {
  behavior?: 'auto' | 'smooth';
  top?: number;
  left?: number;
}

const ScrollToTop = ({ behavior = 'auto', top = 0, left = 0 }: ScrollToTopProps) => {
  const { pathname } = useLocation();

  useEffect(() => {
    // Scroll to top on route change
    window.scrollTo({
      top,
      left,
      behavior,
    });
  }, [pathname, behavior, top, left]);

  return null;
};

export default ScrollToTop;
