// src/App.js
import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import ChatBox from './components/Chatbox';
import { Box, Switch, Typography } from '@mui/material';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  const handleThemeChange = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box display="flex" justifyContent="space-between" alignItems="center" my={2}>
          <Typography variant="h6">Legal GPT</Typography>
          <Box display="flex" alignItems="center">
            <Typography variant="body1">Dark Mode</Typography>
            <Switch checked={darkMode} onChange={handleThemeChange} />
          </Box>
        </Box>
        <ChatBox />
      </Container>
    </ThemeProvider>
  );
}

export default App;
