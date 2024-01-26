function openModal(title, content) {
    var modal = document.getElementById('myModal');
    var modalContent = document.getElementById('modalContent');
  
    modal.style.display = 'block';
    modalContent.innerHTML = '<h2>' + title + '</h2><p>' + content + '</p>';
  }
  
  function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    var causesList = document.getElementById('causesList');
    var submitButton = document.getElementById('submitButton');
  
    causesList.addEventListener('change', function () {
      var selectedCause = document.querySelector('input[name="cause"]:checked');
      if (selectedCause) {
        submitButton.style.display = 'block';
        document.body.style.backgroundColor = 'black';
        document.body.style.color = 'white';
      } else {
        submitButton.style.display = 'none';
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
      }
    });
  });
  