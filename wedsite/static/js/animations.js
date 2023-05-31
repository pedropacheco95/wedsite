
function showProgress() {
    let progress_bars = document.querySelectorAll('.progressBar_fill');
    progress_bars.forEach((bar) => {
        let value = bar.dataset.progress;
        bar.style.opacity = 1;
        bar.style.width = `${value}%`;
    });
}

function appearOnScroll() {
    let reveals = document.querySelectorAll('.appearing')

    reveals.forEach((reveal) => {
        let windowHeight = window.innerHeight;
        let revealTop = reveal.getBoundingClientRect().top;
        let revealPoint = 150;

        if (revealTop < windowHeight - revealPoint){
            reveal.classList.add('active');
        }else{
            reveal.classList.remove('active');
        }
    });
}

function showOtherImage(next_previous){
    let current_image = document.querySelector('.image_shown');
    console.log(current_image);
    console.log(next_previous);
    let sibling;
    if (next_previous == 'next'){
        sibling = current_image.nextElementSibling
    }else if (next_previous == 'previous'){
        sibling = current_image.previousElementSibling
    }
    if (sibling.classList.contains('hidden_image')){
        sibling.classList.add('image_shown');
        sibling.classList.remove('hidden_image');
        current_image.classList.remove('image_shown');
        current_image.classList.add('hidden_image');
    }
}

function loaderCheck(){
    let loader = document.querySelector('.circle-loader');
    let checkmark = document.querySelector('.checkmark');
    let message = document.querySelector('.contribution_thank_you');
    let message2 = document.querySelector('.confirmation_thank_you');
    if (!message){
        message = message2;
    }
    if (loader){
        loader.classList.add('load-complete');
        checkmark.style.display = 'block';
        message.style.opacity = 1;
    }
}

function onloadLoaderCheck(){
    setInterval(loaderCheck, 2000);
}

function loadHandler(){
    showProgress();
    appearOnScroll();
    onloadLoaderCheck();
}

function scrollHandler(){
    appearOnScroll();
}

window.addEventListener('load', loadHandler);
window.addEventListener('scroll', scrollHandler);