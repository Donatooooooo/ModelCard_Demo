```
trainer = model_name(target value, [drop column], dataset)
trainer.findBestParams()
print(trainer.getParams())
trainer.run()
print(trainer.getMetrics())
```