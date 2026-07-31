const path = require('path');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/download', (req, res) => {
  const file = path.join(__dirname, 'public', 'downloads', 'JamItDa-Setup-v0.1-beta.exe');
  res.download(file, 'JamItDa-Setup-v0.1-beta.exe');
});

app.listen(PORT, () => {
  console.log(`JAM IT, DA! landing page running on port ${PORT}`);
});
