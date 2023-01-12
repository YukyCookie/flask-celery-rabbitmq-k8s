// Placeholder for dropdowns
const $placeholder = $("select[placeholder]");
if ($placeholder.length) {
  $placeholder.each(function() {
    const $this = $(this);

    // Initial
    $this.addClass("placeholder-shown");
    const placeholder = $this.attr("placeholder");
    $this.prepend(`<option value="" selected style="display: none;" >${placeholder}</option>`);

    // Change
    $this.on("change", (event) => {
      const $this = $(event.currentTarget);
    //   $this.removeClass("placeholder-shown").addClass("placeholder-hidden");
      if ($this.val()) {
        $this.removeClass("placeholder-shown").addClass("placeholder-hidden");
      } else {
        $this.addClass("placeholder-shown").removeClass("placeholder-hidden");
      }
    });
  });
}



document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search_result').style.display="none"
    document.querySelector('#form').onsubmit = () => {
        document.querySelector('#search_list').innerHTML="";
        document.getElementById("senti_piechart").innerHTML = "";
        document.getElementById("wordcloud_div").style.display = "none";
        document.getElementById("search_button").style.display="none"
        document.getElementById("search_hr").style.display="none";

        // Initialize new request
        const request = new XMLHttpRequest();
        window.search_query = document.querySelector('#form-username').value;
        window.search_number = document.querySelector('#form-number').value;
        window.select_search = document.querySelector("#select-search").value;
        window.select_result = document.querySelector('#select-result').value;

        request.open('POST', '/search');
        if (search_query!="" && search_number!="" && select_search!="" && select_result!=""){
            document.getElementById('search_result').style.display="block"
            document.getElementById("loading").style.display = "inline flow-root list-item";
        }
        
        if (select_result == "All Tweets") {
            // Callback function for when request completes
            request.onload = () => {
                
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
                const senti_piechart = document.getElementById("senti_piechart");
                document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();
                
                var pos = data.pos_len;
                var neg = data.neg_len;
                var neu = data.neu_len;
                var opin = data.opi_len;
                var fact = data.fac_len;

                // Update the result div
                if (data.success) {

                    for(var i = 0; i<data.tweets.length ; i++){

                        const li = document.createElement('li');
                        const p = document.createElement('p');
                        // li.innerHTML = data.tweets[i][0];
                        p.innerHTML = data.tweets[i];
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
                    document.getElementById("loading").style.display = "none";
                    document.getElementById("search_hr").style.display="block";
                    document.getElementById("search_button").style.display="block"
                    Plotly.newPlot(senti_piechart, senti_data, senti_layout);
                    document.getElementById("wordcloud_div").style.display = "block";
                }

            }

            // Add data to send with request
            const data = new FormData();
            data.append('search_query', search_query);
            data.append('search_number', search_number);
            data.append('select_search', select_search);
            data.append('select_result', select_result);


            // Send request
            request.send(data);
            return false;
        } else {
            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
                document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();
    
                // Update the result div
                if (data.success) {
    
                    for(var i = 0; i<data.tweets.length ; i++){

                        const li = document.createElement('li');
                        const p = document.createElement('p');
                        // li.innerHTML = data.tweets[i][0];
                        p.innerHTML = data.tweets[i][0];
                        li.append(p);
                        document.querySelector('#search_list').append(li);
                    }
                    document.getElementById("loading").style.display = "none";
                    document.getElementById("search_hr").style.display="block";
                    if (document.getElementById('search_list').getElementsByTagName("li").length > 0){
                        document.getElementById("wordcloud_div").style.display = "block";
                    }
                    
                }
    
            }
    
            // Add data to send with request
            const data = new FormData();
            data.append('search_query', search_query);
            data.append('search_number', search_number);
            data.append('select_search', select_search);
            data.append('select_result', select_result);
    
            // Send request
            request.send(data);
            return false;
        } 

    };

    document.querySelector('#psenti').onclick = () =>{
        const senti = 'p';
        document.querySelector('#search_list').innerHTML="";
        document.getElementById("wordcloud_div").style.display = "none";
        document.getElementById("search_hr").style.display="none";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query1 = document.querySelector('#form-username').value;
        const search_number1 = document.querySelector('#form-number').value;
        const select_search1 = document.querySelector('#select-search').value;
        const select_result1 = document.querySelector('#select-result').value;

        request.open('POST', '/search_pos');
        if (search_query1 !="" && search_number1 !="" && select_search1 !="" && select_result1 !=""){
            document.getElementById('search_result').style.display="block"
            document.getElementById("loading2").style.display = "inline flow-root list-item";
        }
        document.getElementById("loading2").style.display = "inline flow-root list-item";

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);
                }
                document.getElementById("loading2").style.display = "none";
                document.getElementById("search_hr").style.display="block";
                if (document.getElementById('search_list').getElementsByTagName("li").length > 0){
                    document.getElementById("wordcloud_div").style.display = "block";
                }
                
            }

        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query1);
        data.append('search_number', search_number1);
        data.append('select_search', select_search1);
        data.append('select_search', select_result1);

        // Send request
        request.send(data);
        return false;
    };


    document.querySelector('#nsenti').onclick = () =>{
        const senti = 'n';
        document.querySelector('#search_list').innerHTML="";
        document.getElementById("wordcloud_div").style.display = "none";
        document.getElementById("search_hr").style.display="none";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query1 = document.querySelector('#form-username').value;
        const search_number1 = document.querySelector('#form-number').value;
        const select_search1 = document.querySelector('#select-search').value;
        const select_result1 = document.querySelector('#select-result').value;

        request.open('POST', '/search_neg');
        if (search_query1 !="" && search_number1 !="" && select_search1 !="" && select_result1 !=""){
            document.getElementById('search_result').style.display="block"
            document.getElementById("loading2").style.display = "inline flow-root list-item";
        }
        document.getElementById("loading2").style.display = "inline flow-root list-item";

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);
                }
                document.getElementById("loading2").style.display = "none";
                document.getElementById("search_hr").style.display="block";
                if (document.getElementById('search_list').getElementsByTagName("li").length > 0){
                    document.getElementById("wordcloud_div").style.display = "block";
                }
                
            }

        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query1);
        data.append('search_number', search_number1);
        data.append('select_search', select_search1);
        data.append('select_search', select_result1);

        // Send request
        request.send(data);
        return false;
    };



    document.querySelector('#opi').onclick = () =>{
        const opi = 'o';
        document.querySelector('#search_list').innerHTML="";
        document.getElementById("wordcloud_div").style.display = "none";
        document.getElementById("search_hr").style.display="none";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query1 = document.querySelector('#form-username').value;
        const search_number1 = document.querySelector('#form-number').value;
        const select_search1 = document.querySelector('#select-search').value;
        const select_result1 = document.querySelector('#select-result').value;

        request.open('POST', '/search_opi');
        if (search_query1 !="" && search_number1 !="" && select_search1 !="" && select_result1 !=""){
            document.getElementById('search_result').style.display="block"
            document.getElementById("loading2").style.display = "inline flow-root list-item";
        }
        document.getElementById("loading2").style.display = "inline flow-root list-item";

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);
                }
                document.getElementById("loading2").style.display = "none";
                document.getElementById("search_hr").style.display="block";
                if (document.getElementById('search_list').getElementsByTagName("li").length > 0){
                    document.getElementById("wordcloud_div").style.display = "block";
                }
                
            }

        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query1);
        data.append('search_number', search_number1);
        data.append('select_search', select_search1);
        data.append('select_search', select_result1);

        // Send request
        request.send(data);
        return false;
    };


    document.querySelector('#fac').onclick = () =>{
        const opi = 'f';
        document.querySelector('#search_list').innerHTML="";
        document.getElementById("wordcloud_div").style.display = "none";
        document.getElementById("search_hr").style.display="none";

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query1 = document.querySelector('#form-username').value;
        const search_number1 = document.querySelector('#form-number').value;
        const select_search1 = document.querySelector('#select-search').value;
        const select_result1 = document.querySelector('#select-result').value;

        request.open('POST', '/search_fac');
        if (search_query1 !="" && search_number1 !="" && select_search1 !="" && select_result1 !=""){
            document.getElementById('search_result').style.display="block"
            document.getElementById("loading2").style.display = "inline flow-root list-item";
        }
        document.getElementById("loading2").style.display = "inline flow-root list-item";

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            document.getElementById("wordcloud_img").src = "../static/img/wordcloud.svg?t="+Math.random();

            // Update the result div
            if (data.success) {

                for(var i = 0; i<data.tweets.length ; i++){
                    const li = document.createElement('li');
                    const p = document.createElement('p');
                    // li.innerHTML = data.tweets[i][0];
                    p.innerHTML = data.tweets[i][0];
                    li.append(p);
                    document.querySelector('#search_list').append(li);
                }
                document.getElementById("loading2").style.display = "none";
                document.getElementById("search_hr").style.display="block";
                if (document.getElementById('search_list').getElementsByTagName("li").length > 0){
                    document.getElementById("wordcloud_div").style.display = "block";
                }
                
            }

        }

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query1);
        data.append('search_number', search_number1);
        data.append('select_search', select_search1);
        data.append('select_search', select_result1);

        // Send request
        request.send(data);
        return false;
    };

    document.querySelector('#res').onclick = () =>{
        document.getElementById('search_result').style.display="none"
        window.search_query = "";
        window.search_number = "";
        window.select_search = "";
        window.select_result = "";
        
        $placeholder.each(function() {
            const $this = $(this);
        
            // Initial
            $this.addClass("placeholder-shown").removeClass("placeholder-hidden");
            const placeholder = $this.attr("placeholder");
        })
        
    };
});

