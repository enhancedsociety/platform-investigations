

<es-avatar>

    <a href="mailto:{opts.email}" class="card">
        <h3>{ opts.email }</h3>
        <img src="{this.img_src}"></img>
    </a>

    <style>
        :scope {
            word-break: break-all;
        }
        a {
            color: initial;
            text-decoration: none;
        }
        .card {
            background: #fff;
            border-radius: 2px;
            display: inline-flex;
            padding: 1rem;
            margin: 1rem;
            width: 20vw;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            transition: all 0.3s cubic-bezier(.25,.8,.25,1);
            align-items: center;
            justify-content: space-evenly;
            flex-direction: column;
        }
        .card:hover {
            box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
        }
    </style>

    <script>
        this.img_src = `https://www.gravatar.com/avatar/${md5(opts.email)}?d=robohash`
    </script>
</es-avatar>
