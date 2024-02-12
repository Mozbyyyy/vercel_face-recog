// Branch Details 

let branchhead = document.querySelector('.branch-head');

let branchinfo2 = document.querySelector('.branch-info2');

let branchimage = document.querySelector('.branch-image');
setTimeout(() => {
    branchhead.classList.add('slide-in');
}, 100);
setTimeout(() => {
    branchimage.classList.add('slide-in-branch-image');
}, 200);
setTimeout(() => {
    branchinfo2.classList.add('slide-in-branchinfo2');
}, 100);
