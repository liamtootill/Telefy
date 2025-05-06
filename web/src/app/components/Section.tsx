import React, { ReactNode } from 'react';
import { useInView } from 'react-intersection-observer';

interface SectionProps {
  children: ReactNode;
  className?: string;
}

const Section: React.FC<SectionProps> = ({ children, className = '' }) => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.15,
  });

  return (
    <section
      ref={ref}
      className={`transition-all duration-1000 ease-out transform opacity-0 translate-y-2 ${
        inView ? 'opacity-100 translate-y-0' : ''
      } ${className}`}
      tabIndex={-1}
      aria-label="Section"
    >
      {children}
    </section>
  );
};

export default Section; 