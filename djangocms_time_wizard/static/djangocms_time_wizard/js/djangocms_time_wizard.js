// https://stackoverflow.com/a/24004942/6836173
const TimeWizardDebounce = function (func, wait, immediate = false) {
  // 'private' variable for instance
  // The returned function will be able to reference this due to closure.
  // Each call to the returned function will share this common timer.
  let timeout
  // Calling debounce returns a new anonymous function
  return function () {
    // reference the context and args for the setTimeout function
    const context = this
    const args = arguments
    // Should the function be called now? If immediate is true
    // and not already in a timeout then the answer is: Yes
    const callNow = immediate && !timeout
    // This is the basic debounce behaviour where you can call this
    // function several times, but it will only execute once
    // (before or after imposing a delay).
    // Each time the returned function is called, the timer starts over.
    clearTimeout(timeout)
    // Set the new timeout
    timeout = setTimeout(function () {
      // Inside the timeout function, clear the timeout variable
      // which will let the next execution run when in 'immediate' mode
      timeout = null
      // Check if the function already ran with the immediate flag
      if (!immediate) {
        // Call the original function with apply
        // apply lets you define the 'this' object as well as the arguments
        // (both captured before setTimeout)
        func.apply(context, args)
      }
    }, wait)
    // Immediate mode and no wait timer? Execute the function...
    if (callNow) func.apply(context, args)
  }
}

// Replace time-wizard-comments with a div.
// -> Reason for this replacement: prevent the cms from setting up its editing-
//    logic on the time-wizard-div. If the div is added in the html directly,
//    you can only double click the wrapper (if present), but not the underlying
//    plugins.
const setupDjangoCMSTimeWizardWrapper = function () {
  // iterate through matching comments and replace them with a div
  const iterator = document.createNodeIterator(
    document.body,
    NodeFilter.SHOW_COMMENT,
    {
      acceptNode: (node) => node.nodeValue.trim().includes('time-wizard-insertion-point')
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_SKIP
    },
    false
  )
  let comment
  while (comment = iterator.nextNode()) {
    let cls = comment.data.includes('-start') ? 'start' : 'end'
    const instanceId = comment.data.replace('time-wizard-insertion-point-start', '').replace('time-wizard-insertion-point-end', '').trim()
    const $el = $('<div class="time-wizard time-wizard-' + cls + '" data-instance-id="' + instanceId + '"></div>')[0]
    comment.parentNode.insertBefore($el, comment)
    comment.remove()
  }

  // set position/size and hover-effects depending on the next sibling
  $('.time-wizard.time-wizard-start').each(function () {
    const wrapper = $(this)
    const instanceId = wrapper.data('instance-id')
    const nextPlugin = $(wrapper.find('+ *')[0])
    const areaEnd = $('.time-wizard.time-wizard-end[data-instance-id="' + instanceId + '"]')

    let wrapperArea = null
    const onMouseMove = function (e) {
      if (
        e.clientX < wrapperArea.left ||
        e.clientX > wrapperArea.right ||
        e.clientY < wrapperArea.top ||
        e.clientY > wrapperArea.bottom
      ) {
        wrapper.css('display', 'block')
        $(document).off('mousemove', onMouseMove)
      }
    }
    const addHover = function () {
      wrapperArea = wrapper[0].getBoundingClientRect()
      wrapper.css('display', 'none')
      $(document).on('mousemove', onMouseMove)
    }
    wrapper.on('mouseenter', addHover)

    const updateStyling = function () {
      wrapper.removeClass('hide')

      const offsetLeft = nextPlugin[0].offsetLeft
      const offsetTop = nextPlugin[0].offsetTop
      const offsetHeight = areaEnd[0].offsetTop - offsetTop
      const offsetWidth = nextPlugin[0].offsetWidth

      wrapper.css(
        {
          'height': offsetHeight + 'px',
          'left': offsetLeft + 'px',
          'top': offsetTop + 'px',
          'width': offsetWidth + 'px',
        }
      )
    }
    let intervalId
    const styleForVisibility = function () {
      if (nextPlugin.is(':visible')) {
        updateStyling()
        stopInterval(intervalId)
      }
    }

    // periodically check the sibling for visibility and set styling accordingly
    intervalId = setInterval(styleForVisibility, 500)
    const stopInterval = function () {
      clearInterval(intervalId)
    }

    styleForVisibility()
    $(window).on('resize', TimeWizardDebounce(updateStyling, 200))
    $(window).on('scroll', TimeWizardDebounce(updateStyling, 200))
  })
}

$(document).ready(setupDjangoCMSTimeWizardWrapper)
