new Ajax.Responders.register({
  onCreate: function(){
    alert('a request has been initialized!');
  },
  onComplete: function(){
    alert('a request completed');
  }
});

