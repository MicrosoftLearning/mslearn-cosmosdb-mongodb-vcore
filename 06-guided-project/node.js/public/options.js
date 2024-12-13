class OptionsComponent extends HTMLElement {
    constructor() {
        super();
    }

    // This method runs when the element is inserted into the DOM
    connectedCallback() {
        this.loadOptions();
    }

    // Fetch options from the server and display them
    async loadOptions() {

        try {
            const response = await fetch('/getOptions');
            const options = await response.json();

            const promptWrapper = $('<div>', { class: 'message assistant' });
            const header = $('<div>', { class: 'header' });

            // Create the robot icon element
            const robotIcon = $('<i>', {
                class: 'bi bi-robot',
                'aria-hidden': 'true'
            });

            // Append the icon and the text to the header
            header.append(robotIcon).append(' Assistant');

            const promptText = $('<div>', { class: 'text' }).text('Please select an option:');

            // Create the structure of the custom component
            const wrapper = $('<div>', { class: 'message assistant options-wrapper' });

            options.forEach((option, index) => {
                const button = $('<button>', { class: 'option-item', id: `${index + 1}`, text: option })

                button.on('click', function() {
                    // Call the submitOption function with the button ID
                    submitOption(this.id);
            
                    // Replace the component with the selected message
                    wrapper.html($('<div>', { class: 'selected-option', text: option })); // Replace the content of the chat box
                });

                button.appendTo(wrapper);
            });

            $('.chat-box').append(promptWrapper.append(header).append(promptText));
            $('.chat-box').append(wrapper);

        } catch (error) {
            console.error('Error fetching options:', error);
        }
    }
}

// Define the custom element
customElements.define('custom-options', OptionsComponent);
