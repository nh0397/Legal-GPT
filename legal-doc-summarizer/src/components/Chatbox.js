import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Paper, Typography, IconButton, CircularProgress } from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import config from '../config';
import MessageList from './MessageList';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Clear state variables on refresh
    window.addEventListener('beforeunload', clearLocalStorage);

    // Clear backend messages on component mount
    clearBackendMessages();

    // Fetch messages
    fetchMessages();

    return () => {
      window.removeEventListener('beforeunload', clearLocalStorage);
    };
  }, []);

  const clearLocalStorage = () => {
    localStorage.removeItem('messages');
    localStorage.removeItem('input');
    localStorage.removeItem('file');
  };

  const clearBackendMessages = async () => {
    try {
      await axios.post(`${config.API_BASE_URL}/clear`);
    } catch (error) {
      console.error('Error clearing backend messages', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${config.API_BASE_URL}/messages`);
      setMessages(response.data);
      localStorage.setItem('messages', JSON.stringify(response.data));
    } catch (error) {
      console.error('Error fetching messages', error);
    }
  };

  const handleSend = async () => {
    if (input.trim() !== '' || file) {
      const formData = new FormData();
      formData.append('text', input);
      if (file) {
        formData.append('file', file);
      }

      setLoading(true);

      // Send the message to the backend using fetch to handle streaming
      const response = await fetch(`${config.API_BASE_URL}/messages`, {
        method: 'POST',
        body: formData,
      });

      // Add user message
      const newMessage = {
        text: input,
        file: file ? file.name : null,
        user: true
      };
      const updatedMessages = [...messages, newMessage];
      setMessages(updatedMessages);
      localStorage.setItem('messages', JSON.stringify(updatedMessages));
      setInput('');
      setFile(null);
      localStorage.removeItem('input');
      localStorage.removeItem('file');

      // Handle streaming response for PDF extraction or AI response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let extractedText = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        extractedText += chunk;
        console.log(`Received chunk: ${chunk}`);  // Log the received chunk
        setMessages(prevMessages => {
          const lastMessage = prevMessages[prevMessages.length - 1];
          if (lastMessage.user) {
            return [...prevMessages, { text: chunk, user: false }];
          } else {
            const updatedMessages = [...prevMessages];
            updatedMessages[updatedMessages.length - 1].text += chunk;
            localStorage.setItem('messages', JSON.stringify(updatedMessages));
            return updatedMessages;
          }
        });
      }

      setLoading(false);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      toast.error('Please upload a PDF file.');
    } else {
      setFile(selectedFile);
      localStorage.setItem('file', selectedFile);
    }
  };

  const handleFileRemove = () => {
    setFile(null);
    localStorage.removeItem('file');
  };

  return (
    <Paper elevation={3} sx={{ p: 2, height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <MessageList messages={messages} />
      {file && (
        <Box display="flex" alignItems="center" mb={2} p={1} border={1} borderColor="grey.400" borderRadius="4px">
          <Typography variant="body2" component="p" sx={{ flexGrow: 1 }}>
            {file.name}
          </Typography>
          <IconButton size="small" onClick={handleFileRemove}>
            <CloseIcon />
          </IconButton>
        </Box>
      )}
      <Box display="flex" alignItems="center">
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            localStorage.setItem('input', e.target.value);
          }}
          sx={{ mr: 1 }}
        />
        <input
          accept=".pdf"
          style={{ display: 'none' }}
          id="file-input"
          type="file"
          onChange={handleFileChange}
        />
        <label htmlFor="file-input">
          <IconButton color="primary" component="span">
            <AttachFileIcon />
          </IconButton>
        </label>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSend}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Send'}
        </Button>
      </Box>
    </Paper>
  );
}

export default ChatBox;
