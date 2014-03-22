Při prolézání cizího git repozitáře mě nedávno napadla jednoduchá
myšlenka: mít tak příkaz `git-cd`, který by fungoval stejně jako `cd`,
ale s cestami by pracoval relativně k samotnému repozitáři. A ukázalo
se, že to jde (v bashi) poměrně přímočaře zařídit.

<!--break-->

První věc, co bylo potřeba zjistit je cesta k aktuálnímu *git working
tree*, což se nechá vypsat "jednoduše" takto:

``` {.brush: .bash}
$ git rev-parse --show-toplevel
```

Btw přidal jsem si pro to v `.gitconfig` alias `root`, ale není to dál
pro samotnou funkci `git-cd` třeba.

Jelikož chceme měnit aktuální adresář shellu, není jiná cesta než jít
cestou tvorby shell funkce (definované např, v `~/.bashrc`):

``` {.brush: .bash}
git-cd()
{
  if ! GIT_ROOT=$(git rev-parse --show-toplevel); then
    return 1
  fi
  if [[ $# = 0 ]]; then
    cd ${GIT_ROOT}
  elif [[ "$1" = - ]]; then
    cd -
  else
    cd "${GIT_ROOT}/$1"
  fi
}
```

Funkce pak funguje tak, že volání `git-cd` bez parametrů změní aktuální
pracovní adresář na root git repa (pokud se zrovna v nějakém nacházíme)
a jinak se snaží přejít do zadaného adresáře v rámci repozitáře:

``` {.brush: .bash}
$ cd /home/martin/projects/nitrate/trunk/nitrate/docs
$ git root
/home/martin/projects/nitrate
$ git-cd design/Milestone
$ pwd
/home/martin/projects/nitrate/design/Milestone
$ git-cd
$ pwd
/home/martin/projects/nitrate
```

I když funkční, taková funkce není celá bez podpory doplňování. To ale
taky není složité zařídit:

``` {.brush: .bash}
# bash autocompletion for git-cd
_git-cd()
{
  if ! GIT_ROOT=$(git rev-parse --show-toplevel); then
    return 1
  fi
  # current word to complete
  local CUR=${COMP_WORDS[COMP_CWORD]}
  # remove absolute paths
  if [[ "$CUR" =~ ^/ ]]; then
    CUR=${CUR#"/"}
  fi
  COMPREPLY=($(cd $GIT_ROOT; compgen -S '/' -d $CUR))
}
complete -o nospace -F _git-cd git-cd
```

A tím se dostáváme k použitelnému řešení :-)

Menší problém by (pro někoho) mohlo být, že shell funkci není možně
přímo volat přes `git cd` právě proto, že to není skript, ale jen shell
funkce. Což mi ale osobně přijde jako nepodstatný detail. Teoreticky by
se to sice dalo to obejít přes definici další shell funkce `git`, co by
fungovala jako wrapper, např:

``` {.brush: .bash}
git()
{
  if [[ $1 = cd ]]; then
    git-cd "$2"
  else
    /usr/bin/git "$@"
  fi
}
```

Ale pak by přestalo fungovat doplňování v bashi. Možná by to i tak šlo
nějak ohackovat, ale to mi vážně za tu námahu nestojí :)

Jinak pochopitelně nejsem první, koho něco takového napadlo udělat, viz
třeba:

- [a cd command for git projects/](http://www.michaelvobrien.com/blog/2009/01/a-cd-command-for-git-projects/)
- [jumping to git roots/](http://codification.wordpress.com/2011/11/14/jumping-to-git-roots/)
- [cdgit cd relative to git workdir root](http://git.661346.n2.nabble.com/cdgit-cd-relative-to-git-workdir-root-td7596367.html)
  (tohle je zajímavé zejména pro uživatele zsh - obsahuje odkaz na
  velmi podobné řešení, přičemž doplňování řeší kód na 1 řádek ...)

Ale na druhou stranu jsem nenašel, že by něco podobného bylo třeba v
`git/contrib` nebo v bashrc nějaké distribuce.
