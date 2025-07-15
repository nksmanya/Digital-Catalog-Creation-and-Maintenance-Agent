function startVoiceInput(fieldId) {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'hi-IN'; // Set to user’s local language
  recognition.onresult = function(event) {
    document.getElementById(fieldId).value = event.results[0][0].transcript;
  };
  recognition.start();
}
