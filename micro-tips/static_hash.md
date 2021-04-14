python3.3 부터 hash 값이 프로세스마다 달라서 hashlib쓰길 추천
python 에서 hash randomize를 끄고 싶다면, 양 버전 모두 PYTHONHASHSEED 을 0으로 설정하는 것입니다.
하지만, 권장하는 것은 python 의 built-in hash 함수를 쓰지말고, 명시적으로 알 수 있는 hash 함수를 사용하는 것이 훨씬 좋다는 것입니다.(결론은 마지막 한줄!!!)

_Py_HashRandomization_Init 는 Python/bootstrap_hash.c 에 있습니다.
2.7.14와의 차이는 2.7.14에서는 PYTHONHASHSEED 가 없으면 randomize 작업이 없지만,
3.x 에서는 PYTHONHASHSEED 가 설정되어 있으면 그 값으로 seed를,
없으면 pyurandom 을 호출해서 randomize 가 일어나게 된다는 것입니다.
```python
_PyInitError
_Py_HashRandomization_Init(const _PyCoreConfig *config)
{
    void *secret = &_Py_HashSecret;
    Py_ssize_t secret_size = sizeof(_Py_HashSecret_t);
 
    if (_Py_HashSecret_Initialized) {
        return _Py_INIT_OK();
    }
    _Py_HashSecret_Initialized = 1;
 
    if (config->use_hash_seed) {
        if (config->hash_seed == 0) {
            /* disable the randomized hash */
            memset(secret, 0, secret_size);
        }
        else {
            /* use the specified hash seed */
            lcg_urandom(config->hash_seed, secret, secret_size);
        }
    }
    else {
        /* use a random hash seed */
        int res;
 
        /* _PyRandom_Init() is called very early in the Python initialization
           and so exceptions cannot be used (use raise=0).
 
           _PyRandom_Init() must not block Python initialization: call
           pyurandom() is non-blocking mode (blocking=0): see the PEP 524. */
        res = pyurandom(secret, secret_size, 0, 0);
        if (res < 0) {
            return _Py_INIT_USER_ERR("failed to get random numbers "
                                     "to initialize Python");
        }
    }
    return _Py_INIT_OK();
}

```
