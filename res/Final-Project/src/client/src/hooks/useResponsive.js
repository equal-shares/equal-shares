// @mui
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

export default function useResponsive(query, start, end) {
  const theme = useTheme();
  const mediaQuery = useMediaQuery; // Store the useMediaQuery function

  if (query === 'up') {
    return mediaQuery(theme.breakpoints.up(start));
  }

  if (query === 'down') {
    return mediaQuery(theme.breakpoints.down(start));
  }

  if (query === 'between') {
    return mediaQuery(theme.breakpoints.between(start, end));
  }

  return mediaQuery(theme.breakpoints.only(start));
}

export function useWidth() {
  const theme = useTheme();
  const keys = [...theme.breakpoints.keys].reverse();
  const mediaQuery = useMediaQuery; // Store the useMediaQuery function

  return (
    keys.reduce((output, key) => {
      const matches = mediaQuery(theme.breakpoints.up(key));

      return !output && matches ? key : output;
    }, null) || 'xs'
  );
}


// // @mui
// import { useTheme } from '@mui/material/styles';
// import useMediaQuery from '@mui/material/useMediaQuery';

// export default function useResponsive(query, start, end) {
//   const theme = useTheme();

//   const mediaUp = useMediaQuery(theme.breakpoints.up(start));

//   const mediaDown = useMediaQuery(theme.breakpoints.down(start));

//   const mediaBetween = useMediaQuery(theme.breakpoints.between(start, end));

//   const mediaOnly = useMediaQuery(theme.breakpoints.only(start));

//   if (query === 'up') {
//     return mediaUp;
//   }

//   if (query === 'down') {
//     return mediaDown;
//   }

//   if (query === 'between') {
//     return mediaBetween;
//   }

//   return mediaOnly;
// }

// export function useWidth() {
//   const theme = useTheme();

//   const keys = [...theme.breakpoints.keys].reverse();

//   return (
//     keys.reduce((output, key) => {
//       const matches = useMediaQuery(theme.breakpoints.up(key));

//       return !output && matches ? key : output;
//     }, null) || 'xs'
//   );
// }
