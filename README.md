# CodeSync
A small Sublime Text 3 plugin that for now mirror in real time the state of a file, in the future it will allow cooperative editing of file

To get it to work just open a new file and it has to start with:

```python
#@ SYNCCODE STREAM
#@ {
#@  options...
#@ }
```

and on the recive file:
```python
#@ SYNCCODE RECIVE
#@ {
#@  options...
#@ }
```
every line that start with #@ ,except the first one, are considered as options row.

a simple example is:

```python
#@ SYNCCODE STREAM
#@ {
#@     "ip":"192.168.0.4"
#@     "port":53424
#@ }
```
and

```python
#@ SYNCCODE RECIVE
#@ {
#@     "port":53424
#@ }
```



