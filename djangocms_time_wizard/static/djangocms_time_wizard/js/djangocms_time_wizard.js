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
      acceptNode: (node) => node.nodeValue.trim() === 'time-wizard-insertion-point'
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_SKIP
    },
    false
  )
  let comment
  while (comment = iterator.nextNode()) {
    const $el = $('<div class="time-wizard hide"></div>')[0]
    comment.parentNode.insertBefore($el, comment)
    comment.remove()
  }

  // set position/size and hover-effects depending on the next sibling
  $('.time-wizard').each(function () {
    const wrapper = $(this)
    const nextPlugin = $(wrapper.find('+ *')[0])

    // hide/show when hovering the sibling or wrapper itself
    // (when wrapper gets hidden, hover of sibling needs to enable it again)
    const addHover = function () {
      wrapper.css('display', 'none')
    }
    const removeHover = function () {
      wrapper.css('display', 'block')
    }
    wrapper.on('mouseenter', addHover)
    wrapper.on('mouseleave', removeHover)
    nextPlugin.on('mouseenter', addHover)
    nextPlugin.on('mouseleave', removeHover)

    const updateStyling = function () {
      wrapper.removeClass('hide')

      const offsetLeft = nextPlugin[0].offsetLeft
      const offsetTop = nextPlugin[0].offsetTop
      const offsetHeight = nextPlugin[0].offsetHeight
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
    $(window).on('resize', updateStyling)
  })
}

$(document).ready(setupDjangoCMSTimeWizardWrapper)
