// add event listener on load
window.addEventListener('load', () => {
    // get canvas
    const canvas = document.querySelector('#canvas');
    // get canvas context
    const context = canvas.getContext('2d');
    
    // resizing
    // canvas.height = window.innerHeight;
    // canvas.width = window.innerWidth;

    // to know whether we are pressing down on mouse to paint
    let painting = false;

    function startPosition(event){
        painting = true;
        // uncomment to be able to paint dots with mouse clicks (not just mouse moves)
        // kept it like this because not handy when drawing circle
        // paint(event);
    }

    function endPosition(){
        painting = false;
        // reset path to paint
        context.beginPath();
    }

    function getMousePos(canvas, event) {
        var rectangle = canvas.getBoundingClientRect();
        return {
          x: event.clientX - rectangle.left,
          y: event.clientY - rectangle.top
        };
    }

    // function when mouse is down
    function paint(event){
        if(!painting) return;

        // get correct x y location of mouse on canvas
        var mousePos = getMousePos(canvas, event);

        // line width, style (=round), and color
        context.lineWidth = 2;
        context.lineCap = 'round';
        context.strokeStyle = 'white';

        // paint where mouse is
        context.lineTo(mousePos.x, mousePos.y);
        context.stroke();
        context.beginPath();
        context.moveTo(mousePos.x, mousePos.y)
    }   
    
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', endPosition);
    canvas.addEventListener('mousemove', paint);
})

function save(){ 
    const canvas = document.querySelector('#canvas');

    // document.getElementById('image_width').value = canvas.width;
    // document.getElementById('image_height').value = canvas.height;
    document.getElementById('image').value = canvas.toDataURL('image/png');
    document.forms["form_id"].submit(); 
} 

// window.addEventListener('resize', () => {
//     canvas.height = window.innerHeight;
//     canvas.width = window.innerWidth;
// })
