const goingBtn = document.querySelector('#going');
const planingBtn = document.querySelector('#planing');
const goingAndPlaningBtn = document.querySelector('#goingAndPlaning');
const closeEventBtn = document.querySelector('#closeEvent');
const activeBtn = document.querySelector('#activeNote');
const seatTaken = document.querySelector('#seatTaken');
const newAttendee = document.querySelector('#newAttendee');
const newPlanner = document.querySelector('#newPlanner');
const oldAttendee = document.querySelector('#oldAttendee');
const oldPlanner = document.querySelector('#oldPlanner');
const postComment = document.querySelector('#post-comment');
const commentContainer = document.querySelector('#commentContainer');
const deleteComment = document.querySelectorAll('.deleteComment');
const category = document.querySelector('#category');
const allEvents = document.querySelector('.all-event');
const collapsedBtn = document.querySelector('#collapsedBtn');
const cancelGoing = document.querySelectorAll('.cancelGoing');
const planingImportant = document.querySelectorAll('.planing-important');
const importantSection = document.querySelector('.important-sections');
const notImportantSection = document.querySelector('.not-important-section');
const deletePlan = document.querySelectorAll('.delete-plan');
const year = document.querySelector('#year');

const updateInterestRequest = async (type, eventId, url='/interest') =>{
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify({type, eventId})
  });

  if (response.status !== 201){
    throw new Error('Cannot Post Data From Fetch');
  }
  return await response.json();
}

const updateComment = async (type, eventId, content, commentId='none') => {
  const response = await fetch('/comment', {
    method: 'POST',
    body: JSON.stringify({type, eventId, content})
  });

  if (response.status !== 201){
    throw new Error('Cannot Post Data From Fetch');
  }
  return await response.json();
}

const deleteCommentPost = async (type, commentId) => {
  const response = await fetch('/comment', {
    method: 'POST',
    body: JSON.stringify({type, commentId})
  });

  if (response.status !== 201){
    throw new Error('Cannot Post Data From Fetch');
  }
  return await response.json();
}

const updateImportant = async (type, eventId, value) => {
  const response = await fetch('/planing', {
    method: 'POST',
    body: JSON.stringify({type, eventId, value})
  });

  if (response.status !== 201){
    throw new Error('Cannot Post Data From Fetch');
  }
  return await response.json();
}


deleteComment && deleteComment.forEach(comment => {
  comment.addEventListener('click', e => {
    commentId = e.target.dataset.commentid;
    deleteCommentPost('delete', commentId)
      .then(data => {
        if (data.delete === 'success'){
          comment.parentElement.classList.add('d-none');
        }
      });
  })
});

postComment && postComment.addEventListener('submit', e => {
  e.preventDefault();
  const content = e.target.comment.value;
  const eventId = e.target.eventid.value;
  updateComment('add', eventId, content)
    .then(data => {
      const oldContent = commentContainer.innerHTML;
      let newContent = ` 
        <div id ='eachComment'class="each-comment border border-secondary mt-3"> 
          <i class="fas fa-user-circle mr-1"></i> <strong>${data.owner}</strong> : ${data.comment}
          <button id='deleteBtn' data-commentid={{i.id}} class='deleteComment btn btn-danger btn-sm d-block mt-3'>Delete</button>
        </div>
      `;
      newContent += oldContent; 
      commentContainer.innerHTML = newContent;
      e.target.comment.value = '';
    })
})

cancelGoing && cancelGoing.forEach(cancel => {
  cancel.addEventListener('click', e => {
    const eventId = e.target.dataset.eventid;
    updateInterestRequest('cancel', eventId, '/going')
      .then(data => {
        if(data.cancel){
          cancel.parentElement.parentElement.classList.add('d-none');
        }
      });
  })
})


goingBtn && goingBtn.addEventListener('click', e => {
  const eventId = e.target.dataset.eventid
  const user = e.target.dataset.user;
 
  updateInterestRequest('going', eventId)
    .then(data => {
      if (data.going){
        goingBtn.textContent ='Cancel Going';
        goingBtn.classList.remove('btn-primary');
        goingBtn.classList.add('btn-warning');
        const oldContent = oldAttendee.innerHTML;
        let newConent  = ` <li><i class="fas fa-user-circle mr-1"></i> <span>${user}</span></li>`;
        newConent += oldContent;
        oldAttendee.innerHTML = newConent;

      }else{
        goingBtn.textContent ='Going';
        goingBtn.classList.remove('btn-warning');
        goingBtn.classList.add('btn-primary');
        oldAttendee.removeChild(oldAttendee.childNodes[1]);
      }
      seatTaken.innerText = data.seat;
    })
});

planingBtn && planingBtn.addEventListener('click', e => {
  const eventId = e.target.dataset.eventid
  const user = e.target.dataset.user;

  updateInterestRequest('planing', eventId)
  .then(data => {
    if (data.planing){
      planingBtn.textContent ='Cancel Planning';
      planingBtn.classList.remove('btn-success');
      planingBtn.classList.add('btn-warning');
      const oldContent = oldPlanner.innerHTML;
      let newConent  = ` <li><i class="fas fa-user-circle mr-1"></i> <span>${user}</span></li>`;
      newConent += oldContent;
      oldPlanner.innerHTML = newConent;
    }else{
      planingBtn.textContent =  'Planning';
      planingBtn.classList.remove('btn-warning');
      planingBtn.classList.add('btn-success');
      oldPlanner.removeChild(oldPlanner.childNodes[1]);
    }
  })
});

closeEventBtn && closeEventBtn.addEventListener('click', e => {
  const eventId = e.target.dataset.eventid
  updateInterestRequest('active', eventId, '/active')
  .then(data => {
    activeBtn.innerHTML = `<p class='alert alert-danger'>close</p>`
  })
})


category && category.addEventListener('change', () => {
  const categoryOption = category.value;
  for (let i of allEvents.children){
    if (categoryOption === 'All'){
      i.classList.add('d-block');
      i.classList.remove('d-none');
    }else if (i.id !== categoryOption){
      i.classList.add('d-none');
      i.classList.remove('d-block');
    }else{
      i.classList.add('d-block');
      i.classList.remove('d-none');
    }
  }
});


deletePlan && deletePlan.forEach(dp => {
  dp.addEventListener('click', () => {
    // eventId = json.loads(request.body)['eventId']
    // type = json.loads(request.body)['type']
    // event = Event.objects.get(id=eventId)
    const eventId = dp.dataset.eventid;
    const parent = dp.parentElement.parentElement.parentElement;
    updateInterestRequest('planing', eventId)
      .then(data => parent.classList.add('d-none'));
  })
})

planingImportant && planingImportant.forEach(option => {
  option.addEventListener('change', () => {
    eventId = option.dataset.eventid;
    const value = option.value;
    updateImportant('changeImportant', eventId, value)
      .then(data => {
        // const content = option.parentElement.parentElement.parentElement.parentElement;
        // if (value === 'Important'){
        //   if (importantSection.innerHTML){
        //     importantSection.innerHTML += content.innerHTML;
        //   }else{
        //     importantSection.innerHTML = content.innerHTML;
        //   }
        // }else{
        //   if (notImportantSection.innerHTML){
        //     notImportantSection.innerHTML += content.innerHTML;
        //   }else{
        //     notImportantSection.innerHTML = content.innerHTML;
        //   }
        // }
        location.reload();
      });
  })
})


year.innerHTML = new Date().getFullYear();
