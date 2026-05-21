import React from 'react';
import {Composition} from 'remotion';
import {HelloWorld} from './HelloWorld';
import {AITherapistsCourse} from './AITherapistsCourse';

// 100 intro + 5 people × 150 + 100 outro = 950 frames
const AI_COURSE_DURATION = 100 + 5 * 150 + 100;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AITherapistsCourse"
        component={AITherapistsCourse}
        durationInFrames={AI_COURSE_DURATION}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          titleText: 'Hello World',
          titleColor: '#00d4ff',
        }}
      />
    </>
  );
};
