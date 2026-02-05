import React, { useState } from 'react';
import './App.css';
import BusinessProfileForm from './components/BusinessProfileForm';
import FinancialForm from './components/FinancialForm';
import EnhancedDashboard from './components/EnhancedDashboard';
import { TranslationProvider, useTranslation } from './context/TranslationContext';
import { Activity } from 'lucide-react';

function AppContent() {
  const { language, setLanguage, t } = useTranslation();
  const [step, setStep] = useState('profile'); // 'profile', 'financial', 'results'
  const [businessProfile, setBusinessProfile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const languages = [
    { code: 'en', name: t('languages.en'), flag: '🇬🇧' },
    { code: 'hi', name: t('languages.hi'), flag: '🇮🇳' },
    { code: 'ta', name: t('languages.ta'), flag: '🇮🇳' }
  ];

  const handleProfileSubmit = (profile) => {
    setBusinessProfile(profile);
    setStep('financial');
  };

  const handleProfileSkip = () => {
    setBusinessProfile({
      name: 'My Business',
      business_type: 'private_limited',
      industry: 'services',
      size: 'Medium'
    });
    setStep('financial');
  };

  const handleAnalysis = (result) => {
    setAnalysisResult(result);
    setStep('results');
    // Smooth scroll to top
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  };

  const handleReset = () => {
    setStep('profile');
    setBusinessProfile(null);
    setAnalysisResult(null);
  };

  return (
    <div className="App">
      <header style={{
        backgroundColor: 'rgba(15, 23, 42, 0.8)',
        backdropFilter: 'blur(10px)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        borderBottom: '1px solid var(--glass-border)'
      }}>
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={handleReset}>
            <Activity color="var(--accent-color)" size={32} />
            <h1 style={{ fontSize: '1.5rem', margin: 0, background: 'linear-gradient(to right, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              {t('appName')}
            </h1>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            {/* Language Selector */}
            <div style={{ position: 'relative' }}>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  padding: '8px 12px',
                  background: 'var(--bg-card)',
                  border: '1px solid var(--glass-border)',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  fontSize: '0.9rem',
                  cursor: 'pointer'
                }}
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </header>

      <main className="container" style={{ padding: '40px 20px' }}>
        {step === 'profile' && (
          <>
            <div style={{ marginBottom: '40px', textAlign: 'center' }}>
              <h2 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>
                {t('mainHeading')}
              </h2>
              <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', fontSize: '1.1rem' }}>
                {t('mainSubheading')}
              </p>
            </div>
            <BusinessProfileForm onSubmit={handleProfileSubmit} onSkip={handleProfileSkip} />
          </>
        )}

        {step === 'financial' && (
          <>
            <div style={{ marginBottom: '24px', textAlign: 'center' }}>
              <h2 style={{ fontSize: '2rem', marginBottom: '8px' }}>
                {t('financialDataHeading')}
              </h2>
              <p style={{ color: 'var(--text-secondary)' }}>
                {t('financialDataSubheading')}
              </p>
            </div>
            <FinancialForm
              onAnalyze={handleAnalysis}
              businessProfile={businessProfile}
              language={language}
            />
          </>
        )}

        {step === 'results' && analysisResult && (
          <>
            <div style={{ marginBottom: '24px', textAlign: 'center' }}>
              <h2 style={{ fontSize: '2rem', marginBottom: '8px' }}>
                {t('comprehensiveAnalysisHeading')}
              </h2>
              <p style={{ color: 'var(--text-secondary)' }}>
                {businessProfile?.name || 'Your Business'} • {businessProfile?.industry || 'Services'}
              </p>
              <button
                onClick={handleReset}
                className="btn"
                style={{ marginTop: '16px', background: 'transparent', color: 'var(--text-secondary)' }}
              >
                {t('startNewAnalysis')}
              </button>
            </div>
            <EnhancedDashboard data={analysisResult} businessProfile={businessProfile} />
          </>
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '32px 20px',
        borderTop: '1px solid var(--glass-border)',
        marginTop: '64px',
        color: 'var(--text-secondary)',
        fontSize: '0.9rem'
      }}>
        <p>{t('footer.copyright')}</p>
        <p style={{ marginTop: '8px', fontSize: '0.8rem' }}>
          {t('footer.security')}
        </p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <TranslationProvider>
      <AppContent />
    </TranslationProvider>
  );
}

export default App;
