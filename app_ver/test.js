import React from 'react';

function App() {
  const downloadFile = async () => {
    try {
      const response = await fetch('http://localhost:5000/download-file', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'file.txt';  // Set the file name here
      document.body.appendChild(a);
      a.click();
      a.remove();
      
    } catch (error) {
      console.error('There was an error downloading the file:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Download File</h1>
        <button onClick={downloadFile}>Download</button>
      </header>
    </div>
  );
}

export default App;
