'use client';

import { MotionConfig } from 'framer-motion';
import { useEffect } from 'react';
import Link from 'next/link';

import { Hero } from './landing/Hero';
import { SectorsBar } from './landing/SectorsBar';
import { CapabilitiesGrid } from './landing/CapabilitiesGrid';
import { BuildLoop } from './landing/BuildLoop';
import { Footer } from './landing/Footer';

export function LandingPage() {
  useEffect(() => {
    // reveal on scroll
    const io = new IntersectionObserver((es) => es.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    }), { threshold: 0.14, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));

    // nav shadow on scroll
    const hdr = document.getElementById('hdr');
    if (hdr) {
      const handleScroll = () => hdr.classList.toggle('scrolled', window.scrollY > 8);
      window.addEventListener('scroll', handleScroll, { passive: true });
      return () => window.removeEventListener('scroll', handleScroll);
    }
  }, []);

  return (
    <MotionConfig reducedMotion="user">
      <header id="hdr">
        <div className="wrap">
          <nav>
            <Link href="/" className="brand">
              <svg className="mark" viewBox="0 0 32 32" fill="none">
                <path
                  d="M16 4c-5 0-8 3-8 6.5 0 .8-2 1.5-2 4.5 0 2 1.4 3.4 1.4 5C7.4 22 10 24 13 24M16 4c5 0 8 3 8 6.5 0 .8 2 1.5 2 4.5 0 2-1.4 3.4-1.4 5C24.6 22 22 24 19 24M16 4v22M12 15c-2.6 0-4-1.2-4-3M20 15c2.6 0 4-1.2 4-3"
                  stroke="#2B50E0"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              Quoro<em>Mind</em>
            </Link>
            <div className="nav-links">
              <a href="#capabilities">Capabilities</a>
              <a href="#process">How it works</a>
              <a href="#contact">Deployments</a>
              <Link href="/chat" className="btn btn-primary nav-cta">
                Try QuoroMind
              </Link>
            </div>
          </nav>
        </div>
      </header>

      <main>
        <Hero />
        <SectorsBar />
        <CapabilitiesGrid />
        <BuildLoop />
      </main>

      <Footer />
    </MotionConfig>
  );
}
