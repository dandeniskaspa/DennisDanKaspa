import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

export const HelloWorld: React.FC<{titleText: string; titleColor: string}> = ({
  titleText,
  titleColor,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'});
  const scale = interpolate(frame, [0, 30], [0.8, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a1a2e',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          fontFamily: 'sans-serif',
          fontSize: 80,
          fontWeight: 'bold',
          color: titleColor,
          textAlign: 'center',
        }}
      >
        {titleText}
      </div>
      <div
        style={{
          marginTop: 20,
          fontFamily: 'sans-serif',
          fontSize: 32,
          color: 'rgba(255,255,255,0.7)',
          opacity: interpolate(frame, [30, 60], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        }}
      >
        Frame {frame} / {durationInFrames}
      </div>
    </AbsoluteFill>
  );
};
