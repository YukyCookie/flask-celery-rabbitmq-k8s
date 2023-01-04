document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {
        
        document.querySelector('#search_list').innerHTML="";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-username').value;
        const search_number = document.querySelector('#form-number').value;
        const search_prefer = document.querySelector('#form-prefer').value;

        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            const senti_piechart = document.getElementById("senti_piechart");
            var pos = 0;
            var neg = 0;
            var neu = 0;
            var opin = 0;
            var fact = 0;

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    if(data.tweets[i][1] >0){
                        pos = pos + 1 
                    } else if(data.tweets[i][1] <0){
                        neg = neg + 1
                        
                    } else if(data.tweets[i][1] ==0){
                        neu = neu + 1
                    }
                    if(data.tweets[i][2] >= 0.5){
                        opin = opin + 1
                    } else{
                        fact = fact + 1
                    }

                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);
                }

                // Virtualization - polarity
                const senti_data = [{
                    values: [pos, neg, neu],
                    labels: ["Positive", "Negative", "Neutral"],
                    domain: {column: 0},
                    textinfo: "label+percent",
                    textposition: 'inside',
                    type: 'pie'
                    
                }, {
                    values: [opin, fact],
                    labels: ["Opinion", "Factual"],
                    domain: {column: 1},
                    textinfo: "label+percent",
                    textposition: 'inside',
                    type: 'pie'
                }];
                const senti_layout = {
                    title: {
                        'text': "Count of tweets by Sentiment",
                        'x': 0.5,
                        'y': 0.9,
                        'xanchor':'center',
                        'yanchor':'top'
                    },
                    autosize: true,
                    height: 400,
                    grid: {rows: 1, columns: 2, pattern: 'independent'}
                };
                Plotly.newPlot(senti_piechart, senti_data, senti_layout)
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);
        data.append('search_number', search_number);
        data.append('search_prefer', search_prefer);

        // Send request
        request.send(data);
        return false;

    };

    document.querySelector('#psenti').onclick = () =>{
        const senti = 'p';
        document.querySelector('#search_list').innerHTML="";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-username').value;
        const search_number = document.querySelector('#form-number').value;
        const search_prefer = document.querySelector('#form-prefer').value;
        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    if(data.tweets[i][1] >0){
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);}
                }
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);
        data.append('search_number', search_number);
        data.append('search_prefer', search_prefer);

        // Send request
        request.send(data);
        return false;
   };


    document.querySelector('#nsenti').onclick = () =>{
        const senti = 'n';
        document.querySelector('#search_list').innerHTML="";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-username').value;
        const search_number = document.querySelector('#form-number').value;
        const search_prefer = document.querySelector('#form-prefer').value;
        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    if(data.tweets[i][1] <0){
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);}
                }
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);
        data.append('search_number', search_number);
        data.append('search_prefer', search_prefer);

        // Send request
        request.send(data);
        return false;
   };



    document.querySelector('#opi').onclick = () =>{
        const opi = 'o';
        document.querySelector('#search_list').innerHTML="";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-username').value;
        const search_number = document.querySelector('#form-number').value;
        const search_prefer = document.querySelector('#form-prefer').value;
        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    if(data.tweets[i][2] >= 0.5){
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);}
                }
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);
        data.append('search_number', search_number);
        data.append('search_prefer', search_prefer);

        // Send request
        request.send(data);
        return false;
   };


    document.querySelector('#fac').onclick = () =>{
        const opi = 'f';
        document.querySelector('#search_list').innerHTML="";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-username').value;
        const search_number = document.querySelector('#form-number').value;
        const search_prefer = document.querySelector('#form-prefer').value;
        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    if(data.tweets[i][2] < 0.5){
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);}
                }
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);
        data.append('search_number', search_number);
        data.append('search_prefer', search_prefer);
        
        // Send request
        request.send(data);
        return false;
   };
});