import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from 'remotion';
import {PersonSlide} from './PersonSlide';

// ─── עדכן כאן את שמות המשתתפים ותפקידיהם ───────────────────────────────────
// אחרי הוספת תמונות ל-public/ — הוסף photo: 'person1.jpg' וכו' לכל אובייקט
const PEOPLE = [
  {name: 'דניס דן קספה', title: 'מומחה בינה מלאכותית', accent: '#7c3aed'},
  {name: 'שם מנחה', title: 'תפקיד / התמחות', accent: '#0891b2'},
  {name: 'שם מנחה', title: 'תפקיד / התמחות', accent: '#be185d'},
  {name: 'שם מנחה', title: 'תפקיד / התמחות', accent: '#b45309'},
  {name: 'שם מנחה', title: 'תפקיד / התמחות', accent: '#047857'},
];
// ────────────────────────────────────────────────────────────────────────────

const INTRO_FRAMES = 100;   // ~3.3s
const PERSON_FRAMES = 150;  // 5s each
const OUTRO_FRAMES = 100;   // ~3.3s

// Floating particles background
const ParticleField: React.FC<{frameOffset?: number}> = ({frameOffset = 0}) => {
  const frame = useCurrentFrame() + frameOffset;
  return (
    <AbsoluteFill style={{backgroundColor: '#050510'}}>
      {Array.from({length: 24}).map((_, i) => {
        const angle = (i / 24) * Math.PI * 2;
        const radius = 30 + (i % 4) * 15;
        const speed = 0.008 + (i % 3) * 0.004;
        const x = 50 + radius * Math.cos(angle + frame * speed);
        const y = 50 + radius * Math.sin(angle + frame * speed * 0.7);
        const size = 1.5 + (i % 3);
        const pulse = 0.4 + 0.4 * Math.sin(frame * 0.06 + i * 1.3);
        const color = i % 3 === 0 ? '#7c3aed' : i % 3 === 1 ? '#00d4ff' : '#a78bfa';
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: `${x}%`,
              top: `${y}%`,
              width: size,
              height: size,
              borderRadius: '50%',
              backgroundColor: color,
              opacity: pulse,
              boxShadow: `0 0 ${size * 5}px ${color}`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

// Intro screen
const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const mainSpring = spring({frame, fps, config: {damping: 55, stiffness: 70}});
  const subtitleFade = interpolate(frame, [35, 65], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const taglineFade = interpolate(frame, [55, 85], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const lineWidth = interpolate(mainSpring, [0, 1], [0, 560]);
  const glowPulse = 0.4 + 0.3 * Math.sin(frame * 0.08);
  const exitOpacity = interpolate(frame, [85, 100], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{opacity: exitOpacity}}>
      <ParticleField />

      {/* Grid overlay */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(124,58,237,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(124,58,237,0.08) 1px, transparent 1px)',
          backgroundSize: '90px 90px',
        }}
      />

      {/* Center radial glow */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 60% 50% at 50% 50%, rgba(124,58,237,${0.25 * glowPulse}) 0%, transparent 70%)`,
        }}
      />

      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          gap: 20,
          direction: 'rtl',
        }}
      >
        {/* AI badge */}
        <div
          style={{
            padding: '8px 32px',
            border: '2px solid rgba(124,58,237,0.7)',
            borderRadius: 40,
            fontFamily: 'sans-serif',
            fontSize: 18,
            letterSpacing: 6,
            color: '#a78bfa',
            opacity: mainSpring,
            marginBottom: 8,
          }}
        >
          ARTIFICIAL INTELLIGENCE
        </div>

        {/* Main headline */}
        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 88,
            fontWeight: 900,
            color: '#ffffff',
            textAlign: 'center',
            lineHeight: 1.1,
            transform: `scale(${interpolate(mainSpring, [0, 1], [0.7, 1])})`,
            opacity: mainSpring,
            textShadow: `0 0 60px rgba(124,58,237,${glowPulse * 0.8})`,
          }}
        >
          בינה מלאכותית
        </div>

        {/* Animated line */}
        <div
          style={{
            width: lineWidth,
            height: 4,
            background: 'linear-gradient(90deg, transparent, #7c3aed 20%, #00d4ff 50%, #7c3aed 80%, transparent)',
            borderRadius: 2,
            marginTop: 4,
            marginBottom: 4,
          }}
        />

        {/* Subtitle */}
        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 56,
            fontWeight: 700,
            color: '#c4b5fd',
            textAlign: 'center',
            opacity: subtitleFade,
          }}
        >
          למטפלים
        </div>

        {/* Tagline */}
        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 28,
            color: 'rgba(255,255,255,0.5)',
            textAlign: 'center',
            marginTop: 12,
            opacity: taglineFade,
          }}
        >
          הדרך החדשה לשדרג את הפרקטיקה שלך
        </div>
      </AbsoluteFill>

      {/* Top/bottom bars */}
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 5, background: 'linear-gradient(90deg, #7c3aed, #00d4ff, #7c3aed)'}} />
      <div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: 5, background: 'linear-gradient(90deg, #00d4ff, #7c3aed, #00d4ff)'}} />
    </AbsoluteFill>
  );
};

// Outro / CTA screen
const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const mainSpring = spring({frame, fps, config: {damping: 60}});
  const btnSpring = spring({frame: Math.max(0, frame - 35), fps, config: {damping: 55}});
  const glowPulse = 0.5 + 0.4 * Math.sin(frame * 0.1);

  return (
    <AbsoluteFill>
      <ParticleField />

      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 70% 60% at 50% 50%, rgba(124,58,237,${0.3 * glowPulse}) 0%, transparent 70%)`,
        }}
      />

      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          gap: 28,
          direction: 'rtl',
        }}
      >
        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 36,
            color: '#a78bfa',
            letterSpacing: 4,
            opacity: interpolate(mainSpring, [0, 1], [0, 1]),
          }}
        >
          הצטרפו עכשיו
        </div>

        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 80,
            fontWeight: 900,
            color: '#ffffff',
            textAlign: 'center',
            lineHeight: 1.15,
            transform: `scale(${interpolate(mainSpring, [0, 1], [0.8, 1])})`,
            opacity: mainSpring,
            textShadow: `0 0 50px rgba(124,58,237,${glowPulse})`,
          }}
        >
          קורס בינה מלאכותית
          {'\n'}למטפלים
        </div>

        <div
          style={{
            width: interpolate(mainSpring, [0, 1], [0, 500]),
            height: 4,
            background: 'linear-gradient(90deg, #7c3aed, #00d4ff)',
            borderRadius: 2,
          }}
        />

        {/* CTA Button */}
        <div
          style={{
            marginTop: 16,
            padding: '22px 72px',
            background: 'linear-gradient(135deg, #7c3aed, #00d4ff)',
            borderRadius: 60,
            fontFamily: 'sans-serif',
            fontSize: 30,
            fontWeight: 800,
            color: '#ffffff',
            transform: `scale(${interpolate(btnSpring, [0, 1], [0.7, 1])})`,
            opacity: btnSpring,
            boxShadow: `0 10px 50px rgba(124,58,237,${glowPulse * 0.7})`,
          }}
        >
          לפרטים ורישום
        </div>
      </AbsoluteFill>

      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 5, background: 'linear-gradient(90deg, #7c3aed, #00d4ff, #7c3aed)'}} />
    </AbsoluteFill>
  );
};

// Main composition
export const AITherapistsCourse: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#050510'}}>
      <Sequence from={0} durationInFrames={INTRO_FRAMES}>
        <Intro />
      </Sequence>

      {PEOPLE.map((person, i) => (
        <Sequence
          key={i}
          from={INTRO_FRAMES + i * PERSON_FRAMES}
          durationInFrames={PERSON_FRAMES}
        >
          <PersonSlide {...person} />
        </Sequence>
      ))}

      <Sequence
        from={INTRO_FRAMES + PEOPLE.length * PERSON_FRAMES}
        durationInFrames={OUTRO_FRAMES}
      >
        <Outro />
      </Sequence>
    </AbsoluteFill>
  );
};
