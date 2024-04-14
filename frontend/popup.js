

document.getElementById('checkURL').addEventListener('click', async () => {    
    const resultDiv = document.getElementById('result');
    const resultDiv0 = document.getElementById('result0');
    var textInput = document.getElementById('inputText').value;
    resultDiv0.textContent = 'validatig URL';
    console.log('Check button clicked'); // Log when the button is clicked
    let [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    console.log('Current tab:', tab); // Log the tab object to verify URL is accessible
    if (tab.url && tab.url.includes("youtube.com/watch") ) {
        console.log('Sending request to backend with URL:', tab.url); // Log the URL being sent
            try {
                const response = await fetch('http://localhost:8000/val_url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    // body: JSON.stringify({url: tab.url,textInput:String(textInput)}),
                    body: JSON.stringify({url: tab.url}),
                });
                const data = await response.json();
                document.getElementById('showHide').style.display ="block";
                document.getElementById('result0').textContent = data.results

                document.getElementById('checkButton').addEventListener('click', async () => {
                    
                    if(data.results =="video is ready to search"){
                        textInput =document.getElementById('inputText').value;
                        if(textInput != ''){
                            try {
                                const response = await fetch('http://localhost:8000/yt_search', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({textInput:textInput}),

                                });
                                const data = await response.json();
                                resultDiv.textContent = data.result;
                                // if (data.result.includes('Yes')) {
                                //     resultDiv.classList.add('alert-danger');
                                // }else{
                                //     resultDiv.classList.add('alert-success');
                                // }
                                document.getElementById('result').textContent = data.result
                                resultDiv.style.display = 'block';
                            } catch (error) {
                                console.error('Error:', error); // Log any errors encountered during fetch
                                document.getElementById('result').textContent = 'Error checking URL.';
                            }
                        }else{
                            document.getElementById('result').textContent = 'Error checking URL.';
                        }
                    }else{
                        document.getElementById('result').textContent = 'url is not validated';

                        resultDiv.style.display = 'block';
                    }
                })
            } catch (error) {
                console.error('Error:', error); // Log any errors encountered during fetch
                document.getElementById('result0').textContent = 'Error checking URL.';
            }


    } else {
        console.log('No URL found in current tab'); // Log if no URL is found
        resultDiv0.textContent ="this is not a youtube video link";
        resultDiv0.style.display = 'block';
    }
});
