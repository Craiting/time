function update(){
    percentLeftover = document.querySelector('#percent_left');
    num = 100;
    inds = document.querySelectorAll('.ind-perc');
    ind_percents = [];
    for (i = 0; i < inds.length; i++){
        if (parseInt(inds[i].value) > 0){
            ind_percents.push(parseInt(inds[i].value));
        }
    }
    for (i = 0; i < ind_percents.length; i++){
        num -= ind_percents[i];
    }
    percentLeftover.innerHTML = String(num) + '%';
}