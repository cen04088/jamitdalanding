const path = require('path');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('trust proxy', 1);

app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] === 'http') {
    return res.redirect(301, `https://${req.headers.host}${req.originalUrl}`);
  }
  next();
});

app.use(express.static(path.join(__dirname, 'public')));

app.get('/download', (req, res) => {
  const file = path.join(__dirname, 'public', 'downloads', 'jamitda.exe');
  res.download(file, 'jamitda.exe');
});

app.listen(PORT, () => {
  console.log(`JAM IT, DA! landing page running on port ${PORT}`);
});
