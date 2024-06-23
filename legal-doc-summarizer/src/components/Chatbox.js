import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Paper, Typography, IconButton } from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import config from '../config';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${config.API_BASE_URL}/messages`);
      setMessages(response.data);
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

      try {
        const response = await axios.post(`${config.API_BASE_URL}/messages`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        setMessages([...messages, response.data]);
        setInput('');
        setFile(null);
      } catch (error) {
        console.error('Error sending message', error);
      }
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      toast.error('Please upload a PDF file.');
    } else {
      setFile(selectedFile);
    }
  };

  const handleFileRemove = () => {
    setFile(null);
  };

  return (
    <Paper elevation={3} sx={{ p: 2, height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2 }}>
        {messages.map((message, index) => (
          <Box key={index} my={1}>
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
          </Box>
        ))}
      </Box>
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
          onChange={(e) => setInput(e.target.value)}
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
        <Button variant="contained" color="primary" onClick={handleSend}>
          Send
        </Button>
      </Box>
    </Paper>
  );
}

export default ChatBox;
