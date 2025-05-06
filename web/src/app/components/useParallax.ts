import { useEffect, useRef, useState } from 'react';

const useParallax = (speed: number = 0.1) => {
  const ref = useRef<HTMLDivElement | null>(null);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (!ref.current) return;
      const rect = ref.current.getBoundingClientRect();
      // relativeY: 0 when at top of viewport, positive as it scrolls up
      const relativeY = rect.top;
      setOffset(relativeY * speed);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    // Also update on resize
    window.addEventListener('resize', handleScroll);
    // Initial call
    handleScroll();
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
    };
  }, [speed]);

  return {
    ref,
    style: {
      transform: `translateY(${offset}px)`,
      willChange: 'transform',
    },
  };
};

export default useParallax; 