let selectedOption = 0;

function printAssistantMessage(text) {
    const promptWrapper = $('<div>', { class: 'message assistant' });
    const header = $('<div>', { class: 'header' });

    const robotIcon = $('<i>', {
        class: 'bi bi-robot',
        'aria-hidden': 'true'
    });

    header.append(robotIcon).append(' Assistant');
    const promptText = $('<div>', { class: 'text' }).html(text.replace(/\n/g, '<br>'));
    $('.chat-box').append(promptWrapper.append(header).append(promptText));
    scrollToBottom();
}

function submitOption(optionId) {
    selectedOption = optionId;
    
    fetch(`/submitOption?o=${optionId}`)
    .then(response => response.json())
    .then(data => {

        console.log(data);
        printAssistantMessage(data.result);

        const interval = setInterval(function() {
            $.get('/checkStatus', { taskId: data.taskId })
            .done(function(statusData) {

                console.log("Task status:", statusData.status);

                if (statusData.status === 'completed') {

                    // Stop polling once completed
                    clearInterval(interval); 
                    printAssistantMessage("Operation complete.");

                    // Wait 2 seconds before displaying the options
                    setTimeout(function() {
                        displayOptions();
                    }, 2000);
                }
                
            })
            .fail(function(xhr) {

                if (xhr.status === 404) {
                    // If task not found, stop polling
                    clearInterval(interval);
                    console.error("Task ID not found. Stopping polling.");
                } else {
                    console.error("An error occurred while checking task status.");
                    printAssistantMessage("An error occurred.");
                    clearInterval(interval);
                }

            });
        }, 2000); // Poll every 2 seconds
    })
    .catch(error => console.error('Error:', error));
}

function submitQuery(query) {    

    // Wait 1 second before displaying the message
    setTimeout(function() {
        printAssistantMessage("Please wait");
    }, 1000);
        
    fetch(`/submitQuery?o=${selectedOption}&q=${query}`)
    .then(response => response.json())
    .then(data => {

        // remove the please wait message
        $('.chat-box .message').last().remove();

        console.log(data);
        printAssistantMessage(data.result);

        // Wait 2 seconds before displaying the options
        setTimeout(function() {
            displayOptions();
        }, 2000); 

    })
    .catch(error => console.error('Error:', error));
}

function displayOptions() {
    $('.chat-box').append('<custom-options></custom-options>');
    setTimeout(function() {
        scrollToBottom();
    }, 200);
}

function scrollToBottom() {
    var chatBox = $('.chat-box');
    chatBox.scrollTop(chatBox.prop('scrollHeight'));
}

$('#userInput').keydown(function(event) {
    // Check if the enter key is pressed
    if (event.key === 'Enter' || event.keyCode === 13) { 
        $('#sendBtn').click(); 
    }
});

$('#sendBtn').on('click', function() {
    const userInput = $('#userInput').val();
    
    if (userInput.trim() !== '') {
        console.log(`User Input: ${userInput}`);

        const promptWrapper = $('<div>', { class: 'message user' });
        const header = $('<div>', { class: 'header' });

        const icon = $('<i>', {
            class: 'bi bi-person',
            'aria-hidden': 'true'
        });

        header.append(icon).append(' User');
        const promptText = $('<div>', { class: 'text' }).text(userInput);
        $('.chat-box').append(promptWrapper.append(header).append(promptText));
        scrollToBottom();

        $('#userInput').val('');
        submitQuery(userInput);
    }
});

$('.minimize-btn').click(function() {
    const chatBody = $('.chat-box');
    const chatContainer = $('.chat-container');

    if (chatBody.is(':visible')) {

        // Minimize the chat window
        chatContainer.removeClass('full-height'); 
        chatBody.slideUp(); 
        chatContainer.addClass('collapsed-height'); 

        // Reset the expand icon
        $('#expand-icon').removeClass('bi-arrow-down-right-square');
        $('#expand-icon').addClass('bi-arrow-up-left-square');

        // Update the minimize icon
        $('#minimize-icon').removeClass('bi-dash-square');
        $('#minimize-icon').addClass('bi-plus-square');

    } else {

        // Expand the chat window
        chatBody.slideDown();
        chatContainer.removeClass('collapsed-height');

        // Reset the minimize icon
        $('#minimize-icon').removeClass('bi-plus-square');
        $('#minimize-icon').addClass('bi-dash-square');
    }
});

$('.fullheight-btn').click(function() {
    const chatContainer = $('.chat-container');

    // Reset the minimize icon
    $('#minimize-icon').removeClass('bi-plus-square');
    $('#minimize-icon').addClass('bi-dash-square');

    if (chatContainer.hasClass('full-height') || chatContainer.hasClass('collapsed-height')) {

        // Reset to the default height
        chatContainer.removeClass('full-height');
        chatContainer.removeClass('collapsed-height'); 

        // Reset the expand icon
        $('#expand-icon').removeClass('bi-arrow-down-right-square');
        $('#expand-icon').addClass('bi-arrow-up-left-square');

    } else {

        // Apply full height
        chatContainer.removeClass('collapsed-height'); 
        chatContainer.addClass('full-height');

        // Update the expand icon
        $('#expand-icon').removeClass('bi-arrow-up-left-square');
        $('#expand-icon').addClass('bi-arrow-down-right-square');
    }

    // Ensure the chat is displayed
    $('.chat-box').slideDown();
});
