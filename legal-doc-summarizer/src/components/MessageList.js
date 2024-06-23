import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';
import UserIcon from '@mui/icons-material/Person';  // Example icon for user
import LGIcon from '@mui/icons-material/Chat';  // Example icon for LG

const MessageList = ({ messages }) => {
  return (
    <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, p: 2 }}>
      {messages.map((message, index) => (
        <Box
          key={index}
          my={2}
          display="flex"
          justifyContent={message.user ? 'flex-start' : 'flex-end'}
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
              maxWidth: '75%',
            }}
          >
            {message.text && (
              <Typography variant="body1" component="p">
                {message.text}
              </Typography>
            )}
            {message.file && (
              <Typography variant="body2" component="p" color="textSecondary">
                {message.file}
              </Typography>
            )}
            {message.extracted_text && (
              <Typography variant="body2" component="p" color="textPrimary">
                Extracted Text: {message.extracted_text}
              </Typography>
            )}
          </Box>
          {message.user && (
            <Avatar sx={{ bgcolor: 'secondary.main', ml: 1 }}>
              <UserIcon />
            </Avatar>
          )}
        </Box>
      ))}
    </Box>
  );
};

export default MessageList;
