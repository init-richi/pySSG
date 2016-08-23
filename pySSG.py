#######################################
# author: Richard Mietz               #
# ver:  1.0                           #
# date: 23.08.2016                    #
# pySSG.py: builds nearly everything  #
#           except subpages           #
# Copyright 2016 Richard Mietz        #
#######################################
#    This file is part of pySSG.
#
#    pySSG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pySSG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySSG.  If not, see <http://www.gnu.org/licenses/>.
#
#    Diese Datei ist Teil von pySSG.
#
#    pySSG ist Freie Software: Sie können es unter den Bedingungen
#    der GNU General Public License, wie von der Free Software Foundation,
#    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
#    veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#    pySSG wird in der Hoffnung, dass es nützlich sein wird, aber
#    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#    Siehe die GNU General Public License für weitere Details.
#
#    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.

# module import start
import os, fileinput, shutil
# module import end

# functions start

def build_cp_files(delete):
    '''copies files from "contet/files/", "content/subpages/files/", "template/files/" to "web/files", "web/subpages/files/";
    delete='true'-> deletes all prev. "files"-folders in "web/", delete='false'-> overwrites existing files'''
    if delete == 'true':
        folder_content = os.listdir('web/files/')
        folder_content_sub = os.listdir('web/subpages/files/')
        folder_content_style = os.listdir('web/stylesheet')
        if len(folder_content) != 0:
            os.system('rm -r web/files/*')
        if len(folder_content_sub) != 0:
            os.system('rm -r web/subpages/files/*')
        if len(folder_content_style) != 0:
            os.system('rm -r web/stylesheet/*')
        os.system('cp -r template/files web && cp -r content/files web && cp -r content/subpages/files web/subpages && cp -r template/stylesheet web')
    if delete == 'false':
            os.system('cp -rf template/files web && cp -rf content/files web && cp -rf content/subpages/files web/subpages && cp -r template/stylesheet web')

def build_structure(infolder, outfolder):
    '''build basic html structure with 'template.html' as template from infolder in outfolder'''
    ctnt_dlist = os.listdir(infolder)
    for files in ctnt_dlist:
        if files.endswith('.html') | files.endswith('.php'):
            shutil.copy('template/template.html', outfolder+'/'+files)

def rpl_content(wfile, rpl, ctnt):
    '''replaces 'rpl'({spaceholder}) in 'wfile'(webfile) with 'ctnt'(content)'''
    with fileinput.FileInput(wfile, inplace=True) as file:
        for line in file:
            print(line.replace(rpl, ctnt), end="")

def crt_navi(navname, wfile):
    '''creates nav.temp and writes in 'wfiles'(webfiles) in 'folder' '''
    file = open('tmp/''nav.temp', 'a')
    file.write(' <li><a href="'+wfile+'">'+navname+'</a></li>\n')
    file.close()

def rw_content_header(cfile, wfile, folder):
    '''reads header from 'cfile'(contentfile) and writes title in 'wfile'(webfile)'''
    file = open(folder+'/'+cfile, 'r').readlines()
    header = file[1:4]
    title = header[0]
    title = title[6:-1]
    navname = header[1]
    navname = navname[8:-1]
    sidebar = header[2]
    sidebar = sidebar[8:-1]
    rpl_content('web/'+wfile, '{title}', title) # spaceholder '{title}' will be replaced by 'title' from header-data
    crt_navi(navname, wfile)
    if sidebar == 'default':
        file = open('template/default_sidebar.html', 'r').read()
        rpl_content('web/'+wfile, '{sidebar}', file)
    elif sidebar[0:4] == 'nav.':
        of_page = sidebar[4:]




def rw_content_content(cfile, wfile):
    '''writes main-content from 'cfile'(contentfile) to 'wfile'(webfile)'''
    file = open('content/'+cfile, 'r').readlines()
    content = file[5:]
    content = ''.join(str(i) for i in content)
    rpl_content('web/'+wfile, '{content}', content)


# functions end
check = input('Delete all files in "web/files" & "web/subpages/files"? (true/false)')
print('building files...')
build_cp_files(check)
print('done\n\n')
print('building main structure...')
build_structure('content', 'web')
print('done\n\n')
print('building sub structure...')
build_structure('content/subpages/', 'web/subpages/')
print('done\n\n')
cfile_folder = os.listdir('content')
print('building and writing main navigation...\n')
file = open('tmp/nav.temp', 'a')
file.write('<ul>\n')
file.close()
for cfile in cfile_folder:
    if cfile.endswith('.html') | cfile.endswith('.php'):
        wfile = cfile
        rw_content_header(cfile, wfile, 'content')
        rw_content_content(cfile, wfile)
file = open('tmp/nav.temp', 'a')
file.write('</ul>\n')
file.close()
input('Check "tmp/nav.temp", if everythin is at the right place, then hit [ENTER]')
nav_cnt = open('tmp/nav.temp', 'r').readlines()
nav_cnt = ''.join(str(i) for i in nav_cnt)
for cfile in cfile_folder:
    if cfile.endswith('.html') | cfile.endswith('.php'):
        wfile = cfile
        rpl_content('web/'+wfile, '{navigation}', nav_cnt)
print('done\n\n')
print('preparing navigation for subpages...')
with fileinput.FileInput('tmp/nav.temp', inplace=True) as file:
    for line in file:
        print(line.replace('a href="', 'a href="../'), end="")
print('done\n\n')

