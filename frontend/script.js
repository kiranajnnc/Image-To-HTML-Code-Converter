const imageInput = document.getElementById('imageInput');
const convertBtn = document.getElementById('convertBtn');
const codeOutput = document.getElementById('codeOutput');
const preview = document.getElementById('preview');

convertBtn.addEventListener('click', async () => {
    if (!imageInput.files.length) {
        alert('Please select an image first.');
        return;
    }

    const file = imageInput.files[0];
    const reader = new FileReader();

    reader.onload = async () => {
        const base64 = reader.result.split(',')[1]; // Remove data:image/...;base64,

        codeOutput.textContent = 'Generating code...';

        try {
            const response = await fetch('http://localhost:5000/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ imageBase64: base64 }),
            });

            const data = await response.json();

            if (data.error) {
                codeOutput.textContent = 'Error: ' + data.error;
                preview.srcdoc = '';
            } else {
                codeOutput.textContent = data.code;

                // Extract HTML and CSS from the code string
                // For simplicity, assume the AI returns a full HTML document
                preview.srcdoc = data.code;
            }
        } catch (err) {
            codeOutput.textContent = 'Error: ' + err.message;
            preview.srcdoc = '';
        }
    };

    reader.readAsDataURL(file);
});

