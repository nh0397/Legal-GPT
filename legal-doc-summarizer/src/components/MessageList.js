import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';
import UserIcon from '@mui/icons-material/Person';  // Example icon for user
import LGIcon from '@mui/icons-material/Chat';  // Example icon for LG
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import './MessageList.css';

const parseBoldText = (text) => {
  if (!text) return text; // Return if text is undefined or null

  const parts = text.split(/(\*\*[^*]+\*\*)/);
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
};

const formatMessageText = (text) => {
  const lines = text.split('\n');
  return lines.map((line, index) => {
    if (line.startsWith('* ')) {
      const boldPart = line.slice(2).trim();
      return (
        <Box key={index} component="div" sx={{ display: 'flex', alignItems: 'flex-start', ml: 2 }}>
          <Box component="span" sx={{ mr: 1 }}>•</Box>
          <Box component="span"><strong>{parseBoldText(boldPart)}</strong></Box>
        </Box>
      );
    } else {
      return (
        <Box key={index} component="div" sx={{ display: 'block', ml: 2 }}>
          {parseBoldText(line)}
        </Box>
      );
    }
  });
};

const MessageList = ({ messages }) => {
  return (
    <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, p: 2 }}>
      <TransitionGroup>
        {messages.map((message, index) => (
          <CSSTransition
            key={index}
            timeout={500}
            classNames="message"
          >
            <Box
              my={2}
              display="flex"
              justifyContent={message.user ? 'flex-start' : 'flex-end'}
              sx={{ maxWidth: '100%' }} // Allowing full width
            >
              {!message.user && (
                <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                  <LGIcon />
                </Avatar>
              )}
              <Box
                sx={{
                  bgcolor: message.user ? 'grey.300' : 'primary.main',
                  color: message.user ? 'black' : 'white',
                  p: 2,
                  borderRadius: 2,
                  maxWidth: '75%', // Limit width to 75% of the container
                  wordBreak: 'break-word', // Ensure long words are wrapped
                }}
              >
                <Typography variant="body1" component="div" style={{ whiteSpace: 'pre-line' }}>
                  {formatMessageText(message.text)}
                </Typography>
                {message.file && (
                  <Typography variant="body2" component="p" color="textSecondary">
                    {message.file}
                  </Typography>
                )}
              </Box>
              {message.user && (
                <Avatar sx={{ bgcolor: 'secondary.main', ml: 1 }}>
                  <UserIcon />
                </Avatar>
              )}
            </Box>
          </CSSTransition>
        ))}
      </TransitionGroup>
    </Box>
  );
};

export default MessageList;
