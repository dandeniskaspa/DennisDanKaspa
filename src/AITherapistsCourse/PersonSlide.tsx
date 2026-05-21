import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
} from 'remotion';

interface PersonSlideProps {
  photo: string;
  name: string;
  title: string;
  accent?: string;
}

export const PersonSlide: React.FC<PersonSlideProps> = ({
  photo,
  name,
  title,
  accent = '#7c3aed',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const photoSpring = spring({frame, fps, config: {damping: 70, stiffness: 80}});
  const textDelay = Math.max(0, frame - 15);
  const textSpring = spring({frame: textDelay, fps, config: {damping: 60}});

  const photoScale = interpolate(photoSpring, [0, 1], [0.85, 1]);
  const photoOpacity = interpolate(photoSpring, [0, 1], [0, 1]);
  const textX = interpolate(textSpring, [0, 1], [-120, 0]);
  const textOpacity = interpolate(textDelay, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  const lineWidth = interpolate(textSpring, [0, 1], [0, 180]);

  const exitOpacity = interpolate(frame, [130, 150], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{opacity: exitOpacity}}>
      {/* Blurred background */}
      <AbsoluteFill
        style={{
          filter: 'blur(24px)',
          transform: 'scale(1.12)',
          opacity: 0.25,
        }}
      >
        <Img
          src={staticFile(photo)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>

      {/* Gradient overlay */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(135deg, rgba(5,5,16,0.92) 45%, rgba(124,58,237,0.15) 100%)',
        }}
      />

      {/* Grid */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(124,58,237,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(124,58,237,0.07) 1px, transparent 1px)',
          backgroundSize: '80px 80px',
        }}
      />

      {/* Content */}
      <AbsoluteFill
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 80,
          paddingLeft: 80,
          paddingRight: 80,
        }}
      >
        {/* Text block (RTL) */}
        <div
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-end',
            direction: 'rtl',
            transform: `translateX(${textX}px)`,
            opacity: textOpacity,
          }}
        >
          <div
            style={{
              fontFamily: 'sans-serif',
              fontSize: 22,
              letterSpacing: 6,
              color: accent,
              textTransform: 'uppercase',
              marginBottom: 18,
            }}
          >
            מציגים
          </div>

          <div
            style={{
              fontFamily: 'sans-serif',
              fontSize: 64,
              fontWeight: 900,
              color: '#ffffff',
              lineHeight: 1.15,
              textAlign: 'right',
              textShadow: '0 2px 20px rgba(0,0,0,0.5)',
            }}
          >
            {name}
          </div>

          {/* Animated accent line */}
          <div
            style={{
              width: lineWidth,
              height: 4,
              background: `linear-gradient(90deg, ${accent}, #00d4ff)`,
              borderRadius: 2,
              marginTop: 20,
              marginBottom: 20,
            }}
          />

          <div
            style={{
              fontFamily: 'sans-serif',
              fontSize: 32,
              color: '#c4b5fd',
              textAlign: 'right',
              lineHeight: 1.4,
            }}
          >
            {title}
          </div>
        </div>

        {/* Photo */}
        <div
          style={{
            flexShrink: 0,
            width: 400,
            height: 540,
            borderRadius: 24,
            overflow: 'hidden',
            border: `3px solid ${accent}99`,
            boxShadow: `0 0 80px ${accent}55, 0 20px 60px rgba(0,0,0,0.6)`,
            transform: `scale(${photoScale})`,
            opacity: photoOpacity,
          }}
        >
          <Img
            src={staticFile(photo)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              objectPosition: 'top center',
            }}
          />
        </div>
      </AbsoluteFill>

      {/* Top gradient bar */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 5,
          background: `linear-gradient(90deg, ${accent}, #00d4ff, ${accent})`,
        }}
      />

      {/* Course tag bottom */}
      <div
        style={{
          position: 'absolute',
          bottom: 36,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          opacity: textOpacity,
        }}
      >
        <div
          style={{
            fontFamily: 'sans-serif',
            fontSize: 20,
            color: 'rgba(255,255,255,0.45)',
            letterSpacing: 2,
            direction: 'rtl',
          }}
        >
          קורס בינה מלאכותית למטפלים
        </div>
      </div>
    </AbsoluteFill>
  );
};
