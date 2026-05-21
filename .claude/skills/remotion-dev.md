# remotion-dev

Use this skill when the user wants to run, preview, render, or develop Remotion videos in this project.

## Starting the Remotion Studio

Run the development server so the user can preview compositions in the browser:

```bash
npm run dev
# or equivalently:
npx remotion studio
```

The studio opens at http://localhost:3000 by default. It provides a visual timeline, per-frame scrubbing, and hot reload on file changes.

## Project Structure

- `src/index.ts` — entry point; calls `registerRoot`
- `src/Root.tsx` — defines all `<Composition>` components
- `src/*/index.tsx` — individual composition components

## Adding a New Composition

1. Create `src/MyComposition/index.tsx` with a React component that uses Remotion hooks:
   - `useCurrentFrame()` — current frame number (0-based)
   - `useVideoConfig()` — `{ fps, durationInFrames, width, height }`
   - `interpolate(frame, [inRange], [outRange], options)` — map frame to a value
   - `spring({ frame, fps, config })` — physics-based spring animation
   - `<AbsoluteFill>` — full-canvas positioned container

2. Register it in `src/Root.tsx`:
   ```tsx
   <Composition
     id="MyComposition"
     component={MyComposition}
     durationInFrames={150}
     fps={30}
     width={1920}
     height={1080}
     defaultProps={{}}
   />
   ```

## Rendering a Video

```bash
# Render the HelloWorld composition to output.mp4
npx remotion render HelloWorld output.mp4

# Render with custom props
npx remotion render HelloWorld output.mp4 --props='{"titleText":"Custom","titleColor":"#ff0"}'

# Render a still image at frame 30
npx remotion still HelloWorld frame30.png --frame=30
```

## Common Patterns

### Fade in
```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'});
```

### Spring scale
```tsx
import {spring, useVideoConfig} from 'remotion';
const {fps} = useVideoConfig();
const scale = spring({frame, fps, config: {damping: 80}});
```

### Sequence timing
```tsx
import {Sequence} from 'remotion';
<Sequence from={30} durationInFrames={60}>
  <MyComponent />
</Sequence>
```

## Troubleshooting

- If the studio fails to start, check that port 3000 is free.
- TypeScript errors in compositions are shown in the studio; fix them to see the preview.
- Use `npx remotion upgrade` to update all Remotion packages to the latest compatible versions together.
